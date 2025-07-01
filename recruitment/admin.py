from django.contrib import admin
from .models import AuthorityToRecruit, JobPosting, Applicant
from django.http import HttpResponse
import tablib
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

@admin.register(AuthorityToRecruit)
class ATRAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'department', 'status', 'request_date', 'number_of_positions')
    list_filter = ('status', 'department')
    search_fields = ('job_title', 'department')


@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('atr', 'posted_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('atr__job_title',)


@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'job_posting', 'applied_date', 'qualifications_met', 'interview_date',
        'interview_score', 'background_check_status', 'drug_test_result',
        'final_decision', 'offer_date', 'onboarding_completed'
    )
    list_filter = (
        'status', 'qualifications_met', 'background_check_status',
        'psychological_evaluation', 'drug_test_result', 'final_decision', 'onboarding_completed'
    )
    search_fields = (
        'name', 'job_posting__atr__job_title', 'interview_comments',
        'screening_notes', 'background_check_status'
    )
    list_display_links = ('name',)
    actions = ["export_as_excel", "export_as_pdf"]

    def export_as_excel(self, request, queryset):
        data = tablib.Dataset()
        data.headers = [
            'Name', 'Job Posting', 'Applied Date', 'Qualifications Met', 'Interview Date',
            'Interview Score', 'Background Check', 'Drug Test', 'Final Decision', 'Offer Date', 'Onboarding Completed'
        ]
        for obj in queryset:
            data.append([
                obj.name,
                str(obj.job_posting),
                obj.applied_date,
                'Yes' if obj.qualifications_met else 'No',
                obj.interview_date,
                obj.interview_score,
                obj.background_check_status,
                obj.drug_test_result,
                obj.final_decision,
                obj.offer_date,
                'Yes' if obj.onboarding_completed else 'No',
            ])
        response = HttpResponse(data.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=HRMS_Applicants.xlsx'
        return response
    export_as_excel.short_description = "Export Selected to Excel"

    def export_as_pdf(self, request, queryset):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        title = Paragraph("<b>HRMS Recruitment Applicants Report</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        headers = ['Name', 'Job Posting', 'Applied Date', 'Qualifications Met', 'Interview Date',
            'Interview Score', 'Background Check', 'Drug Test', 'Final Decision', 'Offer Date', 'Onboarding Completed']
        data = [headers]
        for obj in queryset:
            data.append([
                obj.name,
                str(obj.job_posting),
                str(obj.applied_date),
                'Yes' if obj.qualifications_met else 'No',
                str(obj.interview_date),
                obj.interview_score,
                obj.background_check_status,
                obj.drug_test_result,
                obj.final_decision,
                str(obj.offer_date),
                'Yes' if obj.onboarding_completed else 'No',
            ])
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5a8dee')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(table)
        doc.build(elements)
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
    export_as_pdf.short_description = "Export Selected to PDF"
