from django.db import models
from employees.models import Employee

class AuthorityToRecruit(models.Model):
    DEPARTMENT_CHOICES = [
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Maintenance', 'Maintenance'),
        ('Ops', 'Operations'),
        ('Stores', 'SupplyChain'),
        # add more departments as needed
    ]

    REQUEST_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('manager_approved', 'Manager Approved'),
        ('hr_approved', 'HR Approved'),
        ('rejected', 'Rejected'),
    ]

    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    job_title = models.CharField(max_length=100)
    reason = models.TextField()
    number_of_positions = models.PositiveIntegerField(default=1)
    urgency = models.CharField(max_length=50, blank=True)
    request_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=REQUEST_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"ATR {self.job_title} - {self.department} ({self.status})"


class JobPosting(models.Model):
    atr = models.OneToOneField(AuthorityToRecruit, on_delete=models.CASCADE, related_name='job_posting')
    description = models.TextField()
    requirements = models.TextField()
    posted_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Job Posting: {self.atr.job_title} - {self.atr.department}"


class Applicant(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    ]
    DECISION_CHOICES = [
        ('Hired', 'Hired'),
        ('Rejected', 'Rejected'),
    ]
    YES_NO = [('Y', 'Yes'), ('N', 'No')]

    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applicants')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    cv = models.FileField(upload_to='applicant_cvs/')
    applied_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    remarks = models.TextField(blank=True)

    # Extended recruitment tracking
    qualifications_met = models.CharField(max_length=1, choices=YES_NO, default='N')
    screening_notes = models.TextField(blank=True)
    interview_date = models.DateField(null=True, blank=True)
    interview_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    interview_comments = models.TextField(blank=True)
    background_check_status = models.CharField(max_length=50, default='In Progress')
    psychological_evaluation = models.CharField(max_length=100, blank=True)
    physical_fitness_test = models.CharField(max_length=100, blank=True)
    drug_test_result = models.CharField(max_length=100, blank=True)
    final_decision = models.CharField(max_length=20, choices=DECISION_CHOICES, blank=True)
    offer_date = models.DateField(null=True, blank=True)
    onboarding_completed = models.CharField(max_length=1, choices=YES_NO, default='N')

    def __str__(self):
        return f"{self.name} - {self.job_posting.atr.job_title} ({self.status})"
