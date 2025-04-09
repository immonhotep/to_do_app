from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import date
from django.urls import reverse


class Task(models.Model):

    STATUS = (

        ('W', 'Waiting'),
        ('I', 'Inprogress'),
        ('S', 'Success'),
        ('F', 'Failed'),
        ('O', 'Overdue'),
    )
   


    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    note = models.TextField(max_length=500,null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(default=timezone.now)
    start_time = models.TimeField()
    due_date = models.DateField(default=timezone.now)
    due_time = models.TimeField()
    status = models.CharField(max_length = 1, choices=STATUS,default="W")

    def __str__(self):

        return f'{self.title}'
    

    @property
    def get_start(self):

        url = reverse('update_task',args=(self.pk,))
        return f'<a href="{url}"><small>{self.start_time}</small><i> ({self.title})</i></a><hr>'
    
    @property
    def get_due(self):

        url = reverse('update_task',args=(self.pk,))
        return f'<a href="{url}"><small>{self.due_time}</small><i> ({self.title})</i></a><hr>'



@receiver(post_save, sender=Task)
def handler_function(sender, instance, created, **kwargs):
    if  created:
        current_date = date.today()
        if instance.due_date < current_date:
            instance.status = "O"
        elif instance.start_date <= current_date:
            instance.status = "I"
        else:
             instance.status = "W"
        instance.save()


class SubTask(models.Model):

    title = models.CharField(max_length=100, null=True, blank=True)
    subnote = models.TextField(max_length=500,null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=False)
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):

        return f'{self.task}-{self.title}-{self.updated}'




