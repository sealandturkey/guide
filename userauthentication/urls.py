from django.urls import path
from .views import login_view, register_view, reset_password_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('reset-password/', reset_password_view, name='reset-password'),
]