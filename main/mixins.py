from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect


class UserIsAnonymous(UserPassesTestMixin):
  
    def test_func(self):
        return self.request.user.is_anonymous
  
    def handle_no_permission(self):

        return redirect('home')