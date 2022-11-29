# Generated by Django 3.2.5 on 2022-11-24 19:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Engineering', '0022_auto_20221124_1752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bon',
            name='bon_quantity_discount',
            field=models.FloatField(default=0.0, verbose_name='خصم كمية'),
        ),
        migrations.AlterField(
            model_name='bon',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 11, 24, 21, 57, 59, 337548), verbose_name='التاريخ'),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 11, 24, 21, 57, 59, 337548), verbose_name='تاريخ الاضافة'),
        ),
    ]
