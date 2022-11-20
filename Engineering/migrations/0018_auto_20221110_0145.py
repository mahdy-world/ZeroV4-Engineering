# Generated by Django 3.2.5 on 2022-11-09 23:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Engineering', '0017_auto_20221110_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='sheet',
            name='overall',
            field=models.FloatField(blank=True, null=True, verbose_name='حسابي'),
        ),
        migrations.AddField(
            model_name='sheet',
            name='quantity',
            field=models.FloatField(blank=True, null=True, verbose_name='الكميات'),
        ),
        migrations.AddField(
            model_name='sheet',
            name='total',
            field=models.FloatField(blank=True, null=True, verbose_name='حساب المورد'),
        ),
        migrations.AlterField(
            model_name='bon',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 11, 10, 1, 45, 32, 546109), verbose_name='التاريخ'),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='date',
            field=models.DateField(default=datetime.datetime(2022, 11, 10, 1, 45, 32, 545110), verbose_name='تاريخ الاضافة'),
        ),
    ]