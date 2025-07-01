from django.urls import path
from . import views

app_name = 'employee_portal'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('payslips/', views.payslips, name='payslips'),
    path('leave/', views.leave, name='leave'),
    path('training/', views.training, name='training'),
    path('performance/', views.performance, name='performance'),
    path('documents/', views.documents, name='documents'),
]
