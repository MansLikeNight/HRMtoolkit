from django.db import models
from employees.models import Employee

class Benefit(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='benefits')
    health_insurance = models.BooleanField(default=False)  # NHIMA
    pension_scheme = models.BooleanField(default=False)    # NAPSA
    fuel_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    housing_allowance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    leave_days_balance = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Benefit"
        verbose_name_plural = "Benefits"

    def __str__(self):
        return f"{self.employee.name} Benefits"
