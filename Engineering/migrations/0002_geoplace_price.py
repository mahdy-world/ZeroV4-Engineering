# Generated by Django 3.2.5 on 2022-10-11 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Engineering', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='geoplace',
            name='price',
            field=models.FloatField(default=0.0, verbose_name='السعر'),
        ),
    ]
