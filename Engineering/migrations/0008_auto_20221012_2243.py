# Generated by Django 3.2.5 on 2022-10-12 20:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Engineering', '0007_auto_20221012_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bon',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 10, 12, 22, 43, 53, 594173), verbose_name='التاريخ'),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 10, 12, 22, 43, 53, 594173), verbose_name='تاريخ الاضافة'),
        ),
    ]
