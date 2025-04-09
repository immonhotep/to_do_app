from django.shortcuts import render,redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework import status
from .serializers import TaskSerializer,SubTaskSerializer,CreateUserSerializer,UserUpdateSerializer,PassWordUpdateSerializer
from rest_framework.exceptions import APIException
from main.models import Task,SubTask
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash,get_user_model,login 
import re
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


@api_view(['GET'])
def ApiSummary(request):
    api_urls = {
        'Api Summary' :'api/',
        'User Register' : 'api/api-auth/register/',
        'User Login' : 'api/api-auth/login/',
        'User Update':'api/api-auth/update-user/',
        'Password Update':'api/api-auth/update-password/',
        'Task List and Create' : 'api/tasks/',
        'Task Detail' : 'api/task/<task-id>/',
        'Task Update' : 'api/task/<task-id>/update/',
        'Task Delete' : 'api/task/<task-id>/delete/',      
        'Sub Task List and Create' : 'api/task/<task-id>/subtasks/',
        'Sub Task Detail' : 'subtask/<subtask-id>/',
        'Sub Task Update' : 'api/subtask/<subtask-id>/delete/',
        'Sub Task Delete' : 'api/subtask/<subtask-id>/update/',
        
    }
    return Response(api_urls)



class UserCreationAPIView(UserPassesTestMixin,generics.GenericAPIView):

    serializer_class = CreateUserSerializer

    def test_func(self):
    
        if self.request.user.is_anonymous:
            return True
        else:
            return False
        
    def handle_no_permission(self):
        return redirect('api-summary')

    def post(self, request):
        
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        password2 = request.data['password2']

        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,30}$"
        pat = re.compile(regex)
        mat = re.search(pat, password)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'This username is occupied'}, status=400)
        elif User.objects.filter(email=email).exists():
            return Response({'error': 'This email is exist'}, status=400)
        elif len(password) < 8:
            return Response({'error': 'This password is too short. It must contain at least 8 characters'}, status=400)
        elif not mat:
            return Response({'error': 'This password is too common'}, status=400)       
        elif password != password2:
            return Response({'error': "Two password fields didn't match "}, status=400)
        
        else:
            user = User.objects.create_user(username=username,email=email,password=password)
            if user is not None:
                return Response({'success': 'User created successfully'}, status=200)
            else:
                return Response({'error': "something went wrong user not created "}, status=400)

   

        
class UserUpdateAPIView(generics.GenericAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserUpdateSerializer

    queryset = User.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.pk)
        return obj

    def get(self, request):
        user = self.get_object()
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)


    def put(self, request):
        pk = self.request.user.pk
        username = request.data['username']
        email = request.data['email']
        first_name = request.data['first_name']
        last_name =  request.data['last_name']
        
        obj = self.get_object()
        
        if User.objects.filter(email=email).exclude(pk=pk).exists():
            return Response({'error': 'Email already exist'}, status=400)
    
        if User.objects.filter(username=username).exclude(pk=pk).exists():
            return Response({'error': 'This username is occupied'}, status=400)

        else:
            obj.username = username
            obj.email = email
            obj.first_name = first_name
            obj.last_name = last_name
            obj.save()
            return Response({'success': 'User update successfully'}, status=200)
        

class PasswordUpdateAPIView(generics.GenericAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = PassWordUpdateSerializer

    queryset = User.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.pk)
        return obj
    
    def put(self, request):
        user = self.get_object()
        old_password = request.data['old_password']
        new_password1 = request.data['new_password1']
        new_password2 = request.data['new_password2']

        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,30}$"
        pat = re.compile(regex)
        mat = re.search(pat, new_password1)

        if not user.check_password(old_password):
            return Response({"old_password": "Old password is wrong"}, status=status.HTTP_400_BAD_REQUEST)
        elif len(new_password1) < 8:
            return Response({"new_password1": "This password is too short. It must contain at least 8 characters"}, status=status.HTTP_400_BAD_REQUEST)
        elif not mat:
            return Response({"new_password1": "This password is too common"}, status=status.HTTP_400_BAD_REQUEST)       
        elif new_password1 != new_password2:
            return Response({"new_password2": "Two password fields didn't match"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            return Response({"detail": "Password updated successfully"},status=status.HTTP_204_NO_CONTENT)
      


class TaskListCreateAPIView(generics.ListCreateAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def filter_queryset(self, queryset):
        queryset = queryset.filter(user=self.request.user)
        return super().filter_queryset(queryset)

    def perform_create(self,serializer):

        title = serializer.validated_data.get('title')
        note = serializer.validated_data.get('note')
        start_date = serializer.validated_data.get('start_date')
        due_date = serializer.validated_data.get('due_date')
        start_time = serializer.validated_data.get('start_time')
        due_time = serializer.validated_data.get('due_time')
        status = serializer.validated_data.get('status')
   
        if due_date < start_date:
            raise APIException("due date need to greater than start date")
                
        if (due_date == start_date) and (due_time < start_time):
            raise APIException("due time need to greater than start time")
                         
        serializer.save(user=self.request.user,title=title,note=note,start_date=start_date,due_date=due_date,start_time=start_time,due_time=due_time,status=status)
        return super().perform_create(serializer)


class TaskDetailAPIView(generics.GenericAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get(pk=self.request.parser_context['kwargs']['pk'])
            return obj
        except:
            raise Http404


    def get(self, request,pk):
        task = self.get_object()
        serializer = TaskSerializer(task)
        return Response(serializer.data)




class TaskUpdateAPIView(generics.GenericAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = TaskSerializer

    queryset = Task.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get(pk=self.request.parser_context['kwargs']['pk'])
            return obj
        except:
            raise Http404
       
        
    def get(self, request,pk):
        task = self.get_object()
        serializer = TaskSerializer(task)
        return Response(serializer.data)


    def put(self, request, pk):

        title = request.data['title']
        note = request.data['note']
        start_date = request.data['start_date']
        due_date =  request.data['due_date']
        start_time = request.data['start_time']
        due_time = request.data['due_time']
        status = request.data['status']

        if due_date < start_date:
            raise APIException("due date need to greater than start date")
                
        if (due_date == start_date) and (due_time < start_time):
            raise APIException("due time need to greater than start time")

        obj = self.get_object()

        obj.title = title
        obj.note = note
        obj.start_date = start_date
        obj.due_date = due_date
        obj.start_time = start_time
        obj.due_time = due_time
        obj.status = status
        obj.save()
        return Response({'success': 'Task update was successfully'}, status=200)



class TaskDeleteAPIView(generics.DestroyAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    lookup_field = 'pk'

    def filter_queryset(self, queryset):
        queryset = queryset.filter(user=self.request.user)
        return super().filter_queryset(queryset)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    

class SubTaskListCreateAPIView(generics.ListCreateAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SubTaskSerializer


    def get_queryset(self):
        pk = self.request.parser_context['kwargs']['pk']
        task = get_object_or_404(Task,pk=pk)
        queryset = SubTask.objects.filter(user=self.request.user,task=task)
        return queryset


    def perform_create(self,serializer):

        pk = self.request.parser_context['kwargs']['pk']
        task = get_object_or_404(Task,pk=pk)

        title = serializer.validated_data.get('title')
        subnote = serializer.validated_data.get('subnote')
        status = serializer.validated_data.get('status')
        
        serializer.save(user=self.request.user,task=task,title=title,subnote=subnote,status=status)
        return super().perform_create(serializer)
    

class SubTaskDetailAPIView(generics.GenericAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get(pk=self.request.parser_context['kwargs']['pk'])
            return obj
        except:
            raise Http404


    def get(self, request,pk):
        subtask = self.get_object()
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)
    


class SubTaskUpdateAPIView(generics.GenericAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = SubTaskSerializer

    queryset = SubTask.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = queryset.get(pk=self.request.parser_context['kwargs']['pk'])  
            return obj
        except:
            raise Http404

    def get(self, request,pk):
        subtask = self.get_object()
        serializer = SubTaskSerializer(subtask)
        return Response(serializer.data)

    def put(self, request, pk):
        
        title = request.data['title']
        subnote = request.data['subnote']
        status = request.data.get('status')  
        if status is not None:
            status = True
        else:
            status = False
               
        obj = self.get_object()
        obj.title = title
        obj.subnote = subnote
        obj.status = status
        obj.save()       
        return Response({'success': 'Sub Task update was successfully'}, status=200)


class SubTaskDeleteAPIView(generics.DestroyAPIView):

    authentication_classes = [SessionAuthentication, BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

    lookup_field = 'pk'

    def filter_queryset(self, queryset):
        queryset = queryset.filter(user=self.request.user)
        return super().filter_queryset(queryset)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)
    


class CreateAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,'user_id': user.pk,'email': user.email})