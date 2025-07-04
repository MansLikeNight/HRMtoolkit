# Generated by Django 5.2.1 on 2025-06-21 09:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employees', '0002_employee_date_joined_employee_department_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basic_pay', models.DecimalField(decimal_places=2, max_digits=12)),
                ('housing_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('transport_allowance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('other_allowances', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('tax_deductions', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('pension_deductions', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('other_deductions', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('employee', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='salary', to='employees.employee')),
            ],
            options={
                'verbose_name': 'Salary',
                'verbose_name_plural': 'Salaries',
            },
        ),
        migrations.CreateModel(
            name='PayrollRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pay_period_start', models.DateField()),
                ('pay_period_end', models.DateField()),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('amount_paid', models.DecimalField(decimal_places=2, max_digits=12)),
                ('paid', models.BooleanField(default=False)),
                ('salary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payroll_records', to='payroll.salary')),
            ],
            options={
                'verbose_name': 'Payroll Record',
                'verbose_name_plural': 'Payroll Records',
                'ordering': ['-payment_date'],
            },
        ),
    ]
