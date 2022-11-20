# Generated by Django 3.2.5 on 2022-11-09 23:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Engineering', '0018_auto_20221110_0145'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheet',
            name='loads_value',
            field=models.FloatField(blank=True, null=True, verbose_name='قيمة العهد'),
        ),
        migrations.AlterField(
            model_name='bon',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 11, 10, 1, 50, 27, 392214), verbose_name='التاريخ'),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 11, 10, 1, 50, 27, 391215), verbose_name='تاريخ الاضافة'),
        ),
    ]
