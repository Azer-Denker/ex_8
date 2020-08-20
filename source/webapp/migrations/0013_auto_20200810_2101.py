# Generated by Django 2.2.13 on 2020-08-10 15:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_auto_20200807_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(10)], verbose_name='Заголовок'),
        ),
    ]