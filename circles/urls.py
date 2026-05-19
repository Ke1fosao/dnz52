from django.urls import path
from . import views

app_name = 'circles'

urlpatterns = [
    path('', views.circles_page, name='circles_page'),
]
