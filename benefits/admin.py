from django.contrib import admin
from .models import Benefit
from django.http import HttpResponse
import tablib
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

@admin.register(Benefit)
class BenefitAdmin(admin.ModelAdmin):
    list_display = (
        'employee', 'health_insurance', 'pension_scheme', 
        'fuel_allowance', 'phone_allowance', 
        'housing_allowance', 'leave_days_balance', 'updated_at'
    )
    search_fields = ('employee__full_name',)
    list_filter = ('health_insurance', 'pension_scheme')
    actions = ["export_as_excel", "export_as_pdf"]

    def export_as_excel(self, request, queryset):
        data = tablib.Dataset()
        data.headers = [
            'Employee', 'Health Insurance', 'Pension Scheme', 'Fuel Allowance',
            'Phone Allowance', 'Housing Allowance', 'Leave Days Balance', 'Last Updated'
        ]
        for obj in queryset:
            data.append([
                str(obj.employee),
                'Yes' if obj.health_insurance else 'No',
                'Yes' if obj.pension_scheme else 'No',
                obj.fuel_allowance,
                obj.phone_allowance,
                obj.housing_allowance,
                obj.leave_days_balance,
                obj.updated_at,
            ])
        response = HttpResponse(data.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=HRMS_Benefits.xlsx'
        return response
    export_as_excel.short_description = "Export Selected to Excel"

    def export_as_pdf(self, request, queryset):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        title = Paragraph("<b>HRMS Benefits Report</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        headers = [
            'Employee', 'Health Insurance', 'Pension Scheme', 'Fuel Allowance',
            'Phone Allowance', 'Housing Allowance', 'Leave Days Balance', 'Last Updated'
        ]
        data = [headers]
        for obj in queryset:
            data.append([
                str(obj.employee),
                'Yes' if obj.health_insurance else 'No',
                'Yes' if obj.pension_scheme else 'No',
                obj.fuel_allowance,
                obj.phone_allowance,
                obj.housing_allowance,
                obj.leave_days_balance,
                str(obj.updated_at),
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
