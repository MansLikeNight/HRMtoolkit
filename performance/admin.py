from django.contrib import admin
from .models import PerformanceReview
from django.http import HttpResponse
import tablib
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = (
        'employee', 'review_period_start', 'review_period_end',
        'overall_rating', 'reviewed_by', 'review_date'
    )
    list_filter = ('overall_rating', 'review_date')
    search_fields = ('employee__full_name', 'reviewed_by')
    actions = ["export_as_excel", "export_as_pdf"]

    def export_as_excel(self, request, queryset):
        data = tablib.Dataset()
        data.headers = [
            'Employee', 'Review Period Start', 'Review Period End', 'Overall Rating', 'Reviewed By', 'Review Date'
        ]
        for obj in queryset:
            data.append([
                str(obj.employee),
                obj.review_period_start,
                obj.review_period_end,
                obj.overall_rating,
                obj.reviewed_by,
                obj.review_date,
            ])
        response = HttpResponse(data.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=HRMS_Performance.xlsx'
        return response
    export_as_excel.short_description = "Export Selected to Excel"

    def export_as_pdf(self, request, queryset):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        title = Paragraph("<b>HRMS Performance Review Report</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        headers = ['Employee', 'Review Period Start', 'Review Period End', 'Overall Rating', 'Reviewed By', 'Review Date']
        data = [headers]
        for obj in queryset:
            data.append([
                str(obj.employee),
                str(obj.review_period_start),
                str(obj.review_period_end),
                obj.overall_rating,
                obj.reviewed_by,
                str(obj.review_date),
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
