from django.db import models
from django.utils import timezone
from employees.models import Employee

class PerformanceReview(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1 to 5 scale

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    review_period_start = models.DateField(default=timezone.now)
    review_period_end = models.DateField(default=timezone.now)

    work_quality = models.IntegerField(choices=RATING_CHOICES, default=0)
    attendance_punctuality = models.IntegerField(choices=RATING_CHOICES, default=0)
    safety_compliance = models.IntegerField(choices=RATING_CHOICES, default=0)
    teamwork_collaboration = models.IntegerField(choices=RATING_CHOICES, default=0)
    communication_skills = models.IntegerField(choices=RATING_CHOICES, default=0)
    initiative_problem_solving = models.IntegerField(choices=RATING_CHOICES, default=0)
    job_knowledge = models.IntegerField(choices=RATING_CHOICES, default=0)
    adaptability_flexibility = models.IntegerField(choices=RATING_CHOICES, default=0)

    goals_met = models.TextField(blank=True, default='')
    supervisor_comments = models.TextField(blank=True, default='')
    overall_rating = models.IntegerField(choices=RATING_CHOICES, default=3)
    reviewed_by = models.CharField(max_length=100, default='Supervisor')
    review_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.employee.full_name} - Review ({self.review_period_start} to {self.review_period_end})"
