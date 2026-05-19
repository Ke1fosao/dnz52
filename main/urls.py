from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    path('contacts/', views.contacts, name='contacts'),
]
