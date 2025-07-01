from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee-list'),
    path('add/', views.employee_add, name='employee-add'),
    path('edit/<int:pk>/', views.employee_edit, name='employee-edit'),
    path('delete/<int:pk>/', views.employee_delete, name='employee-delete'),
]
