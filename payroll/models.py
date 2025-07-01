from django.db import models
from employees.models import Employee

class Salary(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='salary')
    basic_pay = models.DecimalField(max_digits=12, decimal_places=2)
    housing_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    transport_allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pension_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Salary"
        verbose_name_plural = "Salaries"

    def __str__(self):
        return f"{self.employee.name} Salary"

    @property
    def total_allowances(self):
        return self.housing_allowance + self.transport_allowance + self.other_allowances

    @property
    def total_deductions(self):
        return self.tax_deductions + self.pension_deductions + self.other_deductions

    @property
    def net_pay(self):
        return self.basic_pay + self.total_allowances - self.total_deductions


class PayrollRecord(models.Model):
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE, related_name='payroll_records')
    pay_period_start = models.DateField()
    pay_period_end = models.DateField()
    payment_date = models.DateField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Payroll Record"
        verbose_name_plural = "Payroll Records"
        ordering = ['-payment_date']

    def __str__(self):
        return f"Payroll {self.salary.employee.name} {self.pay_period_start} to {self.pay_period_end}"
