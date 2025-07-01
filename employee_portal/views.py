from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from employees.models import Employee
from payroll.models import PayrollRecord
from leave.models import LeaveRequest
from training.models import TrainingRecord
from performance.models import PerformanceReview
from documents.models import Document

@login_required
def dashboard(request):
    employee = Employee.objects.get(user=request.user)
    context = {'employee': employee}
    return render(request, 'employee_portal/dashboard.html', context)

@login_required
def payslips(request):
    employee = Employee.objects.get(user=request.user)
    payslips = PayrollRecord.objects.filter(salary__employee=employee).order_by('-payment_date')
    context = {'payslips': payslips}
    return render(request, 'employee_portal/payslips.html', context)

@login_required
def leave(request):
    employee = Employee.objects.get(user=request.user)
    leaves = LeaveRequest.objects.filter(employee=employee).order_by('-start_date')
    context = {'leaves': leaves}
    return render(request, 'employee_portal/leave.html', context)

@login_required
def training(request):
    employee = Employee.objects.get(user=request.user)
    trainings = TrainingRecord.objects.filter(employee=employee).order_by('-date_completed')
    context = {'trainings': trainings}
    return render(request, 'employee_portal/training.html', context)

@login_required
def performance(request):
    employee = Employee.objects.get(user=request.user)
    reviews = PerformanceReview.objects.filter(employee=employee).order_by('-date')
    context = {'reviews': reviews}
    return render(request, 'employee_portal/performance.html', context)

@login_required
def documents(request):
    employee = Employee.objects.get(user=request.user)
    docs = Document.objects.filter(employee=employee).order_by('-uploaded_at')
    context = {'documents': docs}
    return render(request, 'employee_portal/documents.html', context)
