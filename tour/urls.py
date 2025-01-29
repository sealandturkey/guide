from django.urls import path
from . import views

urlpatterns = [
    path('<str:parameter>/<str:language>/', views.show_page, name='Tours'),
]
