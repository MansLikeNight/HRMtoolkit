from django.contrib import admin
from .models import Employee
from django.http import HttpResponse
import tablib
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'full_name', 'job_title', 'department',
        'hire_date', 'national_id', 'gender',
        'contract_type', 'employee_category', 'point_of_hire'
    ]
    search_fields = ('full_name', 'job_title', 'department', 'national_id')
    list_filter = ('department', 'contract_type', 'employee_category', 'gender')
    actions = ["export_as_excel", "export_as_pdf"]

    def export_as_excel(self, request, queryset):
        data = tablib.Dataset()
        data.headers = [
            'Name', 'Department', 'Job Title', 'Hire Date', 'National ID', 'Gender',
            'Contract Type', 'Contract Start', 'Contract End', 'Category', 'Point of Hire'
        ]
        for emp in queryset:
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
                emp.employee_category,
                emp.point_of_hire,
            ])
        response = HttpResponse(data.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=HRMS_Employee_List.xlsx'
        return response
    export_as_excel.short_description = "Export Selected to Excel"

    def export_as_pdf(self, request, queryset):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        title = Paragraph("<b>HRMS Employee List</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        headers = [
            'Name', 'Department', 'Job Title', 'Hire Date', 'National ID', 'Gender',
            'Contract Type', 'Contract Start', 'Contract End', 'Category', 'Point of Hire'
        ]
        data = [headers]
        for emp in queryset:
            data.append([
                emp.full_name,
                emp.department,
                emp.job_title,
                str(emp.hire_date),
                emp.national_id,
                emp.gender,
                emp.contract_type,
                str(emp.contract_start_date),
                str(emp.contract_end_date),
                emp.employee_category,
                emp.point_of_hire,
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
