# Generated by Django 2.2 on 2021-05-01 06:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20210501_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время создания'),
        ),
        migrations.AlterField(
            model_name='review',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Время изменения'),
        ),
    ]
