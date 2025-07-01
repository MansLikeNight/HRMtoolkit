from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'full_name', 'job_title', 'department', 'hire_date',
            'national_id', 'gender', 'contract_type',
            'employee_category', 'point_of_hire'
        ]
