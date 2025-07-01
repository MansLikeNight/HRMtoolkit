from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from employees.models import Employee
from leave.models import LeaveRequest
from recruitment.models import JobPosting, Applicant
from attendance.models import Attendance
from performance.models import PerformanceReview
from training.models import TrainingRecord
from payroll.models import PayrollRecord
from django.db.models import Count, Q, Avg
from datetime import date, timedelta
import json

# Login View
class CustomLoginView(LoginView):
    template_name = 'dashboard/login.html'

# Logout View
class CustomLogoutView(LogoutView):
    next_page = 'login'

# Dashboard View
@login_required
def dashboard_home(request):
    # Get filter values from GET params
    day = request.GET.get('day')
    department = request.GET.get('department')
    time = request.GET.get('time')
    employee = request.GET.get('employee')

    employees_qs = Employee.objects.all()
    attendance_qs = Attendance.objects.all()
    performance_qs = PerformanceReview.objects.all()
    applicant_qs = Applicant.objects.all()
    training_qs = TrainingRecord.objects.all()
    payroll_qs = PayrollRecord.objects.all()
    leave_qs = LeaveRequest.objects.all()

    # Filter by department
    if department and department != 'Department':
        employees_qs = employees_qs.filter(department__name=department)
        attendance_qs = attendance_qs.filter(employee__department__name=department)
        performance_qs = performance_qs.filter(employee__department__name=department)
        applicant_qs = applicant_qs.filter(job_posting__department__name=department)
        training_qs = training_qs.filter(employee__department__name=department)
        payroll_qs = payroll_qs.filter(employee__department__name=department)
        leave_qs = leave_qs.filter(employee__department__name=department)

    # Filter by employee
    if employee and employee != 'Employee' and employee != 'All Employees':
        employees_qs = employees_qs.filter(full_name=employee)
        attendance_qs = attendance_qs.filter(employee__full_name=employee)
        performance_qs = performance_qs.filter(employee__full_name=employee)
        applicant_qs = applicant_qs.filter(applicant__full_name=employee)
        training_qs = training_qs.filter(employee__full_name=employee)
        payroll_qs = payroll_qs.filter(employee__full_name=employee)
        leave_qs = leave_qs.filter(employee__full_name=employee)

    # Filter by day/time for attendance (example: only today, this week, this month)
    today = date.today()
    if day == 'Today':
        attendance_qs = attendance_qs.filter(date=today)
    elif day == 'This Week':
        week_start = today - timedelta(days=today.weekday())
        attendance_qs = attendance_qs.filter(date__gte=week_start, date__lte=today)
    elif day == 'This Month':
        attendance_qs = attendance_qs.filter(date__month=today.month, date__year=today.year)

    total_employees = employees_qs.count()
    total_departments = employees_qs.values('department').distinct().count()
    pending_leaves = leave_qs.filter(status='pending').count()
    open_positions = JobPosting.objects.filter(is_active=True).count()
    pending_applicants = applicant_qs.filter(status='applied').count()

    # Attendance chart: Present vs Absent (filtered)
    present_count = attendance_qs.values('employee').distinct().count()
    absent_count = total_employees - present_count
    attendance_labels = ['Present', 'Absent']
    attendance_data = [present_count, max(absent_count, 0)]

    # Performance Review chart: Distribution of overall ratings (1-5)
    perf_counts = performance_qs.values('overall_rating').annotate(count=Count('id')).order_by('overall_rating')
    performance_labels = [str(i) for i in range(1, 6)]
    performance_data = [next((x['count'] for x in perf_counts if x['overall_rating'] == i), 0) for i in range(1, 6)]

    # Recruitment chart: Applicants by status
    recruitment_labels = ['Applied', 'Interview', 'Selected', 'Rejected']
    recruitment_data = [
        applicant_qs.filter(status='applied').count(),
        applicant_qs.filter(status='interview').count(),
        applicant_qs.filter(status='selected').count(),
        applicant_qs.filter(status='rejected').count(),
    ]

    # Training chart: Sessions this month vs last month
    first_of_month = today.replace(day=1)
    last_month = (first_of_month - timedelta(days=1)).replace(day=1)
    training_this_month = training_qs.filter(recorded_at__gte=first_of_month).count()
    training_last_month = training_qs.filter(recorded_at__gte=last_month, recorded_at__lt=first_of_month).count()
    training_labels = ['This Month', 'Last Month']
    training_data = [training_this_month, training_last_month]

    # Payroll chart: Processed vs Pending payrolls (for current month)
    payroll_processed = payroll_qs.filter(payment_date__month=today.month, paid=True).count()
    payroll_pending = payroll_qs.filter(payment_date__month=today.month, paid=False).count()
    payroll_labels = ['Processed', 'Pending']
    payroll_data = [payroll_processed, payroll_pending]

    # Leaves chart: Pending, Approved, Rejected
    leaves_labels = ['Pending', 'Approved', 'Rejected']
    leaves_data = [
        leave_qs.filter(status='pending').count(),
        leave_qs.filter(status='approved').count(),
        leave_qs.filter(status='rejected').count(),
    ]

    department_choices = [
        'Sales & Marketing', 'Finance', 'Human Resources', 'Maintenance', 'Operations',
        'Security', 'Research & Development', 'Occupational Health & Safety',
        'Environmental Management', 'Public Relations', 'Information Technology',
        'Supply Chain', 'Other'
    ]

    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'pending_leaves': pending_leaves,
        'open_positions': open_positions,
        'pending_applicants': pending_applicants,
        'attendance_labels': json.dumps(attendance_labels),
        'attendance_data': json.dumps(attendance_data),
        'performance_labels': json.dumps(performance_labels),
        'performance_data': json.dumps(performance_data),
        'recruitment_labels': json.dumps(recruitment_labels),
        'recruitment_data': json.dumps(recruitment_data),
        'training_labels': json.dumps(training_labels),
        'training_data': json.dumps(training_data),
        'payroll_labels': json.dumps(payroll_labels),
        'payroll_data': json.dumps(payroll_data),
        'leaves_labels': json.dumps(leaves_labels),
        'leaves_data': json.dumps(leaves_data),
        'recent_activities': [],  # You can fill this with real activity data if needed
        'employee_list': Employee.objects.all(),
        'department_choices': department_choices,
    }

    return render(request, 'dashboard/index.html', context)
