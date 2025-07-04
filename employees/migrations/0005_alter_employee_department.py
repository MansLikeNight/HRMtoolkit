# Generated by Django 5.2.1 on 2025-07-01 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_employee_contract_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.CharField(choices=[('Sales & Marketing', 'Sales & Marketing'), ('Finance', 'Finance'), ('HR', 'Human Resources'), ('Maintenance', 'Maintenance'), ('Operations', 'Operations'), ('Security', 'Security'), ('R&D', 'Research & Development'), ('OHS', 'Occupational Health & Safety'), ('EMS', 'Environmental Management'), ('Public Relations', 'Public Relations'), ('IT', 'Information Technology'), ('Supply Chain', 'Supply Chain'), ('Other', 'Other')], default='Other', max_length=100),
        ),
    ]
