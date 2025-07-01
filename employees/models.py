from django.db import models

class Employee(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]

    CONTRACT_TYPE_CHOICES = [
        ('Permanent', 'Permanent'),
        ('Fixed Term', 'Fixed Term'),
        ('Short Term', 'Short Term'),
        ('Intern', 'Intern'),
        ('Probation', 'Probation'),
        ('Verbal', 'Verbal'),
        ('Consultant', 'Consultant'),
        ('Temporary', 'Temporary'),
        ('Seasonal', 'Seasonal'),
        ('Apprentice', 'Apprentice'),
        ('Other', 'Other'),
    ]

    DEPARTMENT_CHOICES = [
        ('Sales & Marketing', 'Sales & Marketing'),
        ('Finance', 'Finance'),
        ('HR', 'Human Resources'),
        ('Maintenance', 'Maintenance'),
        ('Operations', 'Operations'),
        ('Security', 'Security'),
        ('R&D', 'Research & Development'),
        ('OHS', 'Occupational Health & Safety'),
        ('EMS', 'Environmental Management'),
        ('Public Relations', 'Public Relations'),
        ('IT', 'Information Technology'),
        ('Supply Chain', 'Supply Chain'),
        ('Other', 'Other'),
    ]

    full_name = models.CharField(max_length=100, default="Unknown Name")
    job_title = models.CharField(max_length=100, default="Unknown Title")
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, default="Other")
    hire_date = models.DateField(null=True, blank=True)
    national_id = models.CharField(max_length=50, default="N/A")
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], default='Male')
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPE_CHOICES, default="Fixed Term")
    contract_start_date = models.DateField(null=True, blank=True)
    contract_period_months = models.PositiveIntegerField(null=True, blank=True, help_text="Contract period in months (for non-permanent)")
    contract_end_date = models.DateField(null=True, blank=True, editable=False)
    employee_category = models.CharField(max_length=50, default="General")
    point_of_hire = models.CharField(max_length=100, default="Not Specified")

    def save(self, *args, **kwargs):
        if self.contract_type != 'Permanent' and self.contract_start_date and self.contract_period_months:
            from datetime import timedelta
            self.contract_end_date = self.contract_start_date + timedelta(days=30*self.contract_period_months)
        else:
            self.contract_end_date = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name

    def get_display_name(self):
        return f"{self.full_name} ({self.department} / {self.job_title})"
