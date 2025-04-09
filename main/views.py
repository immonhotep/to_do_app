from django.shortcuts import render,redirect
from django.views.generic import View,CreateView,ListView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from .forms import UserLoginform,RegisterForm,ResetPasswordForm,CreateTaskForm,UpdateTaskform,CreateSubTaskForm,UpdateSubTaskForm,UserForm,ChangePasswordForm
from .models import Task,SubTask
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import get_object_or_404
from .mixins import UserIsAnonymous
from datetime import date,timedelta
from django.db.models import Q
from django.utils import timezone
from .utils import Calendar
import calendar
from django.utils.safestring import mark_safe

from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
#prevent error related force_text not found
from django.utils.encoding import force_str as force_text




class HomeView(LoginRequiredMixin,View):

    def get(self,request):

        select = request.GET.get('select',None)
        search = request.GET.get('search',"")
        request.session['searching'] = search

        if select is not None:
            if select == "A":
                tasks = Task.objects.filter(user=request.user,title__icontains=search).order_by('-status')
            else:
                tasks = Task.objects.filter(user=request.user,status=select,title__icontains=search).order_by('-due_date') 
            request.session['selection'] = select      
        else:
            tasks = Task.objects.filter(user=request.user).order_by('-status')
                  
        count = tasks.count()
        p = Paginator(tasks,4)
        page = self.request.GET.get('page')

        try:
            tasks = p.page(page)
        except PageNotAnInteger:
            tasks = p.page(1)
        except EmptyPage:
            tasks = p.page(p.num_pages)

        form = CreateTaskForm()
        context = {'form':form,'tasks':tasks,'count':count}
        return render(request,'main/home.html',context)
    
    def post(self,request):

        form = CreateTaskForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user

            if data.due_date < data.start_date:

                messages.error(request,'due date need to greater than start date')
                return redirect('home')

            if (data.due_date == data.start_date) and (data.due_time < data.start_time):
                messages.error(request,'due time need to greater than start time')
                return redirect('home')
            
            data.save()
            messages.success(request,'You saved new to do task')

        else:
            for error in list(form.errors.values()):
                messages.error(request,error)

        return redirect('home')
    

class DeleteTask(LoginRequiredMixin,View):

    def post(self,request,pk):
        task = get_object_or_404(Task,pk=pk)
        if task.user == request.user:
                task.delete()
                messages.success(request,'you successfully removed your task')
        else:
            messages.error(request,'Permission denied')
        return redirect('home')
    

class UpdateTask(LoginRequiredMixin,View):

    def get(self,request,pk):
        task = get_object_or_404(Task,pk=pk)
        if task.user == request.user:
            form = UpdateTaskform(instance=task)  
            context={'form':form,'title':'task','task':task}
        else:
            messages.error(request,'Permission denied')
            return redirect('home')
        return render(request,'main/update_task.html',context)

    def post(self,request,pk):
        task = get_object_or_404(Task,pk=pk)
        if task.user == request.user:
            form = UpdateTaskform(request.POST,instance=task)
            if form.is_valid():
                data = form.save(commit=False)   
                if data.due_date < data.start_date:
                    messages.error(request,'due date need to greater than start date')
                    return redirect('update_task',pk)

                if (data.due_date == data.start_date) and (data.due_time < data.start_time):
                    messages.error(request,'due time need to greater than start time')
                    return redirect('update_task',pk)
                
                form.save()
                messages.success(request,'Task modified')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
        else:
            messages.error(request,'Permission denied')

        return redirect('home')
    


class SetSuccess(LoginRequiredMixin,View):

    def post(self,request,pk):
        task = get_object_or_404(Task,pk=pk)
        if task.user == request.user:
            if task.status != "S":
                task.status = "S"
                task.save()
                messages.success(request,'Task status modified to success')
            else:
                messages.info(request,'Task already success nothing to do')
        else:
            messages.error(request,'Permission denied this task is not yours')
        return redirect('home')

   
class UserLogin(SuccessMessageMixin,LoginView):

    template_name = 'main/login.html'
    form_class = UserLoginform
    redirect_authenticated_user = True
 
    def get_success_message(self, cleaned_data):
         
         return(f'{self.request.user} has been logged in')
    
    def set_overdue(self,request):
        current_date = date.today()
        tasks = Task.objects.filter(user=request.user,due_date__lt=current_date).exclude(Q(status="S")|Q(status="F")|Q(status="O")).update(status="O")

    def set_inprog(self,request):
        current_date = date.today()
        current_time = timezone.now()
        tasks = Task.objects.filter(user=request.user,start_date=current_date,due_time__gt=current_time,status="W").update(status="I")

    
    def form_invalid(self,form):
        
        for key, error in list(form.errors.items()):
            
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(self.request, "You must pass the reCAPTCHA test")
                continue
            messages.error(self.request, error) 

        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        self.set_overdue(self.request)
        self.set_inprog(self.request)
        return reverse('home')
    

class UserLogout(LogoutView):
  
    def get_success_url(self):

        return reverse_lazy('home')
    

class UserSignUp(UserPassesTestMixin,SuccessMessageMixin,CreateView):

    template_name = 'main/signup.html'
    form_class = RegisterForm
    success_message = "%(username)s was created successfully"
    
    def test_func(self):
        if self.request.user.is_anonymous:
            return True
        else:
            return False
    
    def handle_no_permission(self):
        messages.warning(self.request,'You already logged in ')
        return redirect('home')

   
    def form_valid(self, form):  
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        message = render_to_string('settings/account_activation_email.html', {
        'user':user,
        'domain':current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),})
           
        try:
                user.email_user(subject=subject, message=message)
                messages.success(self.request,'To finish registration please check your mailbox including spam folder and follow instructions')
        except:
            messages.error(self.request,'Mail Server Connection problem, please turn to website admin')


        return super().form_valid(form)
   
    def form_invalid(self, form):
        
        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(self.request, "You must pass the reCAPTCHA test")
                continue
            messages.error(self.request, error)
        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('user_login')
    
    
    def get_success_message(self, cleaned_data):

        return self.success_message % dict(
            cleaned_data,
            username=self.object.username
        )


def account_activation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
    except():
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Your registration finished now please login')
        return redirect('user_login')

    else:
        return render(request, 'settings/activation_invalid.html')





class edit_user(LoginRequiredMixin,View):

    def get(self,request):
        user = request.user
        form = UserForm(instance=user)
        context={'form':form}
        return render(request,'main/edit_user.html',context)

    def post(self,request):

        user = request.user
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            data = form.save(commit=False)
            if User.objects.filter(email=data.email).exclude(pk=user.pk).exists():
                messages.error(request,'This email already exist')
                return redirect('edit_user')
            else:
                data.save()
                messages.success(request,f'{user.username} updated')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
        return redirect('edit_user')
    


class ChangePassword(LoginRequiredMixin,SuccessMessageMixin,PasswordChangeView):

    form_class = ChangePasswordForm
    template_name = 'main/password_change.html'

    def get_success_message(self, cleaned_data):
        return('Your password has been changed')
    
    def get_success_url(self):
        return reverse('home')
    
   
    def form_invalid(self, form):
        for error in list(form.errors.values()):
            messages.error(self.request,error) 
            
        return self.render_to_response(self.get_context_data(form=form))



class ResetPasswordView(UserIsAnonymous,SuccessMessageMixin, PasswordResetView):

    form_class = ResetPasswordForm
    template_name = 'settings/password_reset.html'
    email_template_name = 'settings/password_reset_email.html'
    subject_template_name = 'settings/password_reset_subject.txt'

    success_message = "We sent email for you with instructions to change your password." \
                      " if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    
    success_url = reverse_lazy('home')


    def form_invalid(self, form):
        
        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(self.request, "You must pass the reCAPTCHA test")
                continue
            messages.error(self.request, error)
            
        return redirect('password_reset')
    
    
class CalendarView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'main/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(self.request,withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context
    

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return date.today()
    
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


class SubtaskView(LoginRequiredMixin,View):

    def get(self,request,pk):

        task = get_object_or_404(Task,pk=pk)
        if task.user == request.user:
            subtasks = SubTask.objects.filter(task=task).order_by('-updated')
            count = subtasks.count()
            ready = subtasks.filter(status=True).count()

            p = Paginator(subtasks,5)
            page = self.request.GET.get('page')

            try:
                subtasks = p.page(page)
            except PageNotAnInteger:
                subtasks = p.page(1)
            except EmptyPage:
                subtasks = p.page(p.num_pages)


            try:
                percent = (ready/count)*100
            except ZeroDivisionError:
                percent = 0

            form = CreateSubTaskForm()
            context={'form':form,'subtasks':subtasks,'task':task,'percent':percent,'count':count}
            return render(request,'main/subtask.html',context)
        return redirect('home')

       
    def post(self,request,pk):

        task = get_object_or_404(Task,pk=pk)
        if task.user == request.user:
            form = CreateSubTaskForm(request.POST)
            subtask_count = SubTask.objects.filter(task=task).count()

            if subtask_count >= 20:
                messages.error(request,'You added the maximum amount of subtask, unable to add more')
                return redirect('subtask',task.pk)
            
            if form.is_valid:     
                data = form.save(commit=False)
                data.task = task
                data.user = request.user
                data.save()
                messages.success(request,'New subtask has been added')
            else:
                for error in list(form.errors.values()):
                    messages.error(request,error)
            return redirect('subtask',task.pk)
        else:
            messages.error(request,'Permission denied')
            return redirect('home')


class CheckSubTask(LoginRequiredMixin,View):
   
    def post(self,request,pk):

        id_list = request.POST.getlist('subtask')       
        if id_list:
            for id in id_list:
                subtask = get_object_or_404(SubTask,pk=id)
                if subtask.task.user == request.user:
                    subtask.status = True
                    subtask.save()
                else:
                    messages.error(request,'Permission denied') 
                    return redirect('subtask',pk)
            messages.success(request, 'subtasks status changed to success')         
        return redirect('subtask',pk)
    

    
class ResetSubTask(LoginRequiredMixin,View):

    def post(self,request,pk):

        task = get_object_or_404(Task,pk=pk)
        if task.user == request.user:
            subtasks = task.subtask_set.all().update(status=False)
            messages.success(request,'Subtasks reseted')
        else:
            messages.error(request,'Permission denied')
        return redirect('subtask',task.pk)


class RemoveSubTask(LoginRequiredMixin,View):

    def get(self,request,pk):
        
        subtask = get_object_or_404(SubTask,pk=pk)
        if subtask.task.user == request.user:
            subtask.delete()
            messages.success(request,'Subtask removed')
        else:
            messages.error(request,'Permission denied')
        return redirect('subtask',subtask.task.pk)
    
class DeleteAllSubtask(LoginRequiredMixin,View):

    def post(self,request,pk):
        task = get_object_or_404(Task,pk=pk)
        if task.user == request.user:
            subtasks = task.subtask_set.all()
            subtasks.delete()
            messages.success(request,'All subtask removed')
            return redirect('subtask',task.pk)
        
        
class UpdateSubtask(LoginRequiredMixin,View):

    def get(self,request,pk):
        subtask = get_object_or_404(SubTask,pk=pk)
        if subtask.task.user == request.user:
            form = UpdateSubTaskForm(instance=subtask)
            context={'form':form,'title':'subtask'}
            return render(request,'main/update_task.html',context)
        else:
            messages.error(request,'Permission denied')
            return redirect('subtask',subtask.task.pk)

    
    def post(self,request,pk):

        subtask = get_object_or_404(SubTask,pk=pk)
        if subtask.task.user == request.user:
            form = UpdateSubTaskForm(request.POST,instance=subtask)
            if form.is_valid():
                form.save()
                messages.success(request,'Subtask updated')    
        else:
            messages.error(request,'Permission denied')
        return redirect('subtask',subtask.task.pk)