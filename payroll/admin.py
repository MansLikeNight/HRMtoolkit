from django.contrib import admin
from .models import Salary, PayrollRecord
from django.http import HttpResponse
import tablib
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'basic_pay', 'net_pay')

@admin.register(PayrollRecord)
class PayrollRecordAdmin(admin.ModelAdmin):
    list_display = ('salary', 'pay_period_start', 'pay_period_end', 'payment_date', 'amount_paid', 'paid')
    list_filter = ('paid', 'payment_date')
    search_fields = ('salary__employee__name',)
    actions = ["export_as_excel", "export_as_pdf"]

    def export_as_excel(self, request, queryset):
        data = tablib.Dataset()
        data.headers = [
            'Employee', 'Pay Period Start', 'Pay Period End', 'Payment Date', 'Amount Paid', 'Paid'
        ]
        for obj in queryset:
            data.append([
                str(obj.salary.employee),
                obj.pay_period_start,
                obj.pay_period_end,
                obj.payment_date,
                obj.amount_paid,
                'Yes' if obj.paid else 'No',
            ])
        response = HttpResponse(data.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=HRMS_Payroll.xlsx'
        return response
    export_as_excel.short_description = "Export Selected to Excel"

    def export_as_pdf(self, request, queryset):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        title = Paragraph("<b>HRMS Payroll Report</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        headers = ['Employee', 'Pay Period Start', 'Pay Period End', 'Payment Date', 'Amount Paid', 'Paid']
        data = [headers]
        for obj in queryset:
            data.append([
                str(obj.salary.employee),
                str(obj.pay_period_start),
                str(obj.pay_period_end),
                str(obj.payment_date),
                obj.amount_paid,
                'Yes' if obj.paid else 'No',
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
