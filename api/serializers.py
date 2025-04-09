from rest_framework import serializers
from rest_framework.reverse import reverse
from main.models import Task,SubTask
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model,login
from django.contrib.auth.models import User
import re

  



class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True,style={'input_type': 'password'})
    email = serializers.EmailField()
    extra_kwargs = {"email": {"required": True, "allow_null": False}}

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']




class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')
        email = serializers.EmailField()
        extra_kwargs = {"email": {"required": True, "allow_null": False}}
 
        
class PassWordUpdateSerializer(serializers.Serializer):

    old_password = serializers.CharField(write_only=True,style={'input_type': 'password'})
    new_password1 = serializers.CharField(write_only=True,style={'input_type': 'password'})
    new_password2 = serializers.CharField(write_only=True,style={'input_type': 'password'})


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields=('id','user','subtasks_url','edit_url','delete_url','title','note','start_date','start_time','due_date','due_time','status')
        read_only_fields = ('user',)
        extra_kwargs = {"start_date": {"required": True, "allow_null": False},"due_date": {"required": True, "allow_null": False}}
 

    edit_url = serializers.SerializerMethodField(read_only=True)
    delete_url = serializers.SerializerMethodField(read_only=True)
    subtasks_url = serializers.SerializerMethodField(read_only=True)

    def get_edit_url(self,obj):
        request = self.context.get('request')
    
        if request is None:
            return None
        
        return reverse("task-edit",kwargs={"pk":obj.pk},request=request)
    

    def get_delete_url(self,obj):
        request = self.context.get('request')
    
        if request is None:
            return None
        
        return reverse("task-delete",kwargs={"pk":obj.pk},request=request)
    

    def get_subtasks_url(self,obj):
        request = self.context.get('request')
    
        if request is None:
            return None
        
        return reverse("subtask-list",kwargs={"pk":obj.pk},request=request)
    

class SubTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubTask
        fields=('id','user','subtask_edit_url','subtask_delete_url','task','title','subnote','status')
        read_only_fields = ('user','task')
        extra_kwargs = {"title": {"required": True, "allow_null": False}}
    
    subtask_edit_url = serializers.SerializerMethodField(read_only=True)
    subtask_delete_url = serializers.SerializerMethodField(read_only=True)

    def get_subtask_edit_url(self,obj):
        request = self.context.get('request')
    
        if request is None:
            return None
        
        return reverse("subtask-edit",kwargs={"pk":obj.pk},request=request)
    

    def get_subtask_delete_url(self,obj):
        request = self.context.get('request')
    
        if request is None:
            return None
        
        return reverse("subtask-delete",kwargs={"pk":obj.pk},request=request)
    


