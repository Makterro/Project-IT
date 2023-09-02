from django.contrib.auth.views import LogoutView
from django.urls import path

from auth.views import UserRegistrationView, UserLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='userLogin'),
    path('logout/', LogoutView.as_view(), name='logout')
]
