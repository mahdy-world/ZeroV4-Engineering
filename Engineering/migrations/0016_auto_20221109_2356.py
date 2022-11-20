# Generated by Django 3.2.5 on 2022-11-09 21:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Engineering', '0015_auto_20221109_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bon',
            name='car_number',
            field=models.CharField(max_length=50, null=True, verbose_name='رقم الشاحنة'),
        ),
        migrations.AlterField(
            model_name='bon',
            name='car_owner',
            field=models.CharField(max_length=50, null=True, verbose_name='صاحب االشاحنة'),
        ),
        migrations.AlterField(
            model_name='bon',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 11, 9, 23, 56, 4, 533254), verbose_name='التاريخ'),
        ),
        migrations.AlterField(
            model_name='bon',
            name='load_value',
            field=models.FloatField(default=0.0, null=True, verbose_name='العهدة'),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 11, 9, 23, 56, 4, 532255), verbose_name='تاريخ الاضافة'),
        ),
    ]