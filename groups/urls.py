from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('', views.groups_list, name='groups_list'),
    path('<slug:slug>/', views.group_detail, name='group_detail'),
]
