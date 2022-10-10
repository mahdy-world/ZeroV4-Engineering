# Generated by Django 3.2.5 on 2022-10-05 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الاضافة')),
                ('name', models.CharField(max_length=50, verbose_name='اسم الشركة')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='العنوان')),
                ('phone', models.CharField(blank=True, max_length=12, null=True, verbose_name='رقم الهاتف')),
                ('active', models.BooleanField(default=True, verbose_name='نشطة')),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='GeoPlace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الاضافة')),
                ('name', models.CharField(max_length=50, verbose_name='اسم الموقع')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='العنوان')),
                ('phone', models.CharField(blank=True, max_length=12, null=True, verbose_name='رقم الهاتف')),
                ('active', models.BooleanField(default=True, verbose_name='نشط')),
                ('deleted', models.BooleanField(default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Engineering.company', verbose_name='الشركة المسؤولة')),
            ],
        ),
    ]
