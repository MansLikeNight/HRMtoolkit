from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document-list'),
    path('upload/', views.document_upload, name='document-upload'),
]
