# Generated by Django 3.2.5 on 2022-10-15 21:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Engineering', '0002_auto_20221015_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bon',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 10, 15, 23, 18, 16, 781585), verbose_name='التاريخ'),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 10, 15, 23, 18, 16, 781585), verbose_name='تاريخ الاضافة'),
        ),
    ]