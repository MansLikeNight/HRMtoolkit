from django.db import models
from employees.models import Employee

class TrainingProgram(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    provider = models.CharField(max_length=100)
    date = models.DateField()
    certificate_required = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Training Program"
        verbose_name_plural = "Training Programs"

    def __str__(self):
        return f"{self.title} - {self.date}"


class TrainingRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='training_records')
    program = models.ForeignKey(TrainingProgram, on_delete=models.CASCADE, related_name='attendees')
    status = models.CharField(max_length=50, choices=[
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
        ('failed', 'Failed'),
    ])
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    remarks = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Training Record"
        verbose_name_plural = "Training Records"
        unique_together = ('employee', 'program')

    def __str__(self):
        return f"{self.employee.name} - {self.program.title} ({self.status})"
