from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Task
from django.db.models import Q



 
class Calendar(HTMLCalendar):
	
	def __init__(self,year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	
	def formatday(self, day, events):

		events_per_day = events.filter(Q(start_date__day=day)|Q(due_date__day=day))
		d = ''
		for event in events_per_day:

			start_date = str(event.start_date).rsplit('-', 1)[-1].lstrip("0")	
			due_date = str(event.due_date).rsplit('-', 1)[-1].lstrip("0")

			if start_date == str(day):
				if event.status == "S":
					d += f'<li><b class="badge badge-success">(Success)</b><i class="fa fa-hourglass-start" aria-hidden="true"></i>: {event.get_start}</li>'
				elif event.status == "I":
					d += f'<li><b class="badge badge-warning">(Inprogress)</b><i class="fa fa-hourglass-start" aria-hidden="true"></i>: {event.get_start}</li>'
				elif event.status == "F":
					d += f'<b class="badge badge-danger">(Failed)</b><li><i class="fa fa-hourglass-start" aria-hidden="true"></i>: {event.get_start}</li>'
				elif event.status == "W":
					d += f'<b class="badge badge-info">(Waiting)</b><li><i class="fa fa-hourglass-start" aria-hidden="true"></i>: {event.get_start}</li>'
				elif event.status == "O":
					d += f'<b class="badge badge-dark">(Overdue)</b><li><i class="fa fa-hourglass-start" aria-hidden="true"></i>: {event.get_start}</li>'

			if due_date == str(day):

				if event.status == "S":
					d += f'<li><b class="badge badge-success">(Success)</b><i class="fa fa-hourglass-end" aria-hidden="true"></i>: {event.get_due}</li>'
				elif event.status == "I":
					d += f'<li><b class="badge badge-warning">(Inprogress)</b><i class="fa fa-hourglass-end" aria-hidden="true"></i>: {event.get_due}</li>'
				elif event.status == "F":
					d += f'<li><b class="badge badge-danger">(Failed)</b><i class="fa fa-hourglass-end" aria-hidden="true"></i>: {event.get_due}</li>'
				elif event.status == "W":
					d += f'<li><b class="badge badge-info">(Waiting)</b><i class="fa fa-hourglass-end" aria-hidden="true"></i>: {event.get_due}</li>'
				elif event.status == "O":
					d += f'<li><b class="badge badge-dark">(Overdue)</b><i class="fa fa-hourglass-end" aria-hidden="true"></i>: {event.get_due}</li>'

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'
		
	


	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr class="border border-2 border-secondary"> {week} </tr>'


	def formatmonth(self,request,withyear=True):
		events = Task.objects.filter(start_date__year=self.year, start_date__month=self.month,user=request.user)
		
		cal = f'<table  cellpadding="0" cellspacing="0" class="calendar border border-2 border-secondary shadow-custom">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal
