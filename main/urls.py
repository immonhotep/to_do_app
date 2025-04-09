from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [

    path('',HomeView.as_view(),name="home"),
    path('delete/<int:pk>/',DeleteTask.as_view(),name='delete_task'),
    path('update/<int:pk>/',UpdateTask.as_view(),name='update_task'),
    path('success/<int:pk>/',SetSuccess.as_view(),name='set_success'),
    path('signup/',UserSignUp.as_view(),name='user_signup'),
    path('login/',UserLogin.as_view(),name='user_login'),
    path('logout/',UserLogout.as_view(),name='user_logout'),
    path('edit_user/',edit_user.as_view(),name='edit_user'),
    path('change_password/',ChangePassword.as_view(),name='change_password'),

    path('subtask/<int:pk>/',SubtaskView.as_view(),name='subtask'),
    path('check/<int:pk>/',CheckSubTask.as_view(),name='check'),
    path('reset/<int:pk>/',ResetSubTask.as_view(),name="reset_subtasks"),
    path('remove/<int:pk>/',RemoveSubTask.as_view(),name="remove_subtask"),
    path('update_subtask/<int:pk>/',UpdateSubtask.as_view(),name='update_subtask'),
    path('delete_all_subtasks/<int:pk>/',DeleteAllSubtask.as_view(),name='delete_all_subtasks'),

    path('calendar/',CalendarView.as_view(), name='calendar'),
    
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='settings/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='settings/password_reset_complete.html'),name='password_reset_complete'),
    path('account_activation/<uidb64>/<token>', views.account_activation, name='account_activation'),
   
]