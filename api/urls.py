from django.urls import path,include  
from . import views
from . import api
from .api import TaskListCreateAPIView,TaskUpdateAPIView,TaskDeleteAPIView,SubTaskListCreateAPIView,SubTaskUpdateAPIView, \
   SubTaskDeleteAPIView,UserUpdateAPIView,PasswordUpdateAPIView,UserCreationAPIView,CreateAuthToken,TaskDetailAPIView,SubTaskDetailAPIView
from rest_framework.authtoken.views import obtain_auth_token



urlpatterns = [

   path('', api.ApiSummary, name="api-summary"),
   path('tasks/',TaskListCreateAPIView.as_view(),name='task-list'),
   path('task/<int:pk>/',TaskDetailAPIView.as_view(),name='task-detail'),
   path('task/<int:pk>/update/',TaskUpdateAPIView.as_view(),name='task-edit'),
   path('task/<int:pk>/delete/',TaskDeleteAPIView.as_view(),name="task-delete"),
   path('task/<int:pk>/subtasks/',SubTaskListCreateAPIView.as_view(),name='subtask-list'),
   path('subtask/<int:pk>/',SubTaskDetailAPIView.as_view(),name='subtask-detail'),
   path('subtask/<int:pk>/update/',SubTaskUpdateAPIView.as_view(),name="subtask-edit"),
   path('subtask/<int:pk>/delete/',SubTaskDeleteAPIView.as_view(),name="subtask-delete"),
   path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
   path('api-auth/update-user/',UserUpdateAPIView.as_view(),name='update-user'),
   path('api-auth/update-password/',PasswordUpdateAPIView.as_view(),name='update-password'),
   path('api-auth/register/',UserCreationAPIView.as_view(),name="user-register"),

   path('api-auth/api-token-auth/',CreateAuthToken.as_view(), name='api_token_auth'),

]
