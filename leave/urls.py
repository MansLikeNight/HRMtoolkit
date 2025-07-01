from django.urls import path
from . import views

urlpatterns = [
    path('', views.leave_list, name='leave-list'),
    path('new/', views.leave_create, name='leave-create'),
]
