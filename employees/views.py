from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm
from django.http import HttpResponse
import tablib
from io import BytesIO
from reportlab.pdfgen import canvas

def employee_list(request):
    employees = Employee.objects.all()
    export = request.GET.get('export')
    if export == 'excel':
        data = tablib.Dataset()
        data.headers = ['Name', 'Department', 'Job Title', 'Hire Date', 'National ID', 'Gender', 'Contract Type', 'Contract Start', 'Contract End']
        for emp in employees:
            data.append([
                emp.full_name,
                emp.department,
                emp.job_title,
                emp.hire_date,
                emp.national_id,
                emp.gender,
                emp.contract_type,
                emp.contract_start_date,
                emp.contract_end_date,
            ])
        response = HttpResponse(data.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=employees.xlsx'
        return response
    elif export == 'pdf':
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica", 12)
        y = 800
        p.drawString(30, y, "Employee List")
        y -= 30
        headers = ['Name', 'Department', 'Job Title', 'Hire Date', 'National ID', 'Gender', 'Contract Type', 'Contract Start', 'Contract End']
        for i, h in enumerate(headers):
            p.drawString(30 + i*100, y, h)
        y -= 20
        for emp in employees:
            row = [
                str(emp.full_name), str(emp.department), str(emp.job_title), str(emp.hire_date), str(emp.national_id), str(emp.gender), str(emp.contract_type), str(emp.contract_start_date), str(emp.contract_end_date)
            ]
            for i, val in enumerate(row):
                p.drawString(30 + i*100, y, str(val))
            y -= 20
            if y < 50:
                p.showPage()
                y = 800
        p.save()
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
    return render(request, 'employees/employee_list.html', {'employees': employees})

def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee-list')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form})

def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee-list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'employees/employee_form.html', {'form': form})

def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee-list')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee})
