from django.urls import path
from . import views

app_name = 'specialists'

urlpatterns = [
    path('<str:page_type>/', views.specialist_page, name='specialist_page'),
]
