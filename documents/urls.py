from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('', views.documents_list, name='documents_list'),
    path('download/<int:pk>/', views.document_download, name='document_download'),
]
