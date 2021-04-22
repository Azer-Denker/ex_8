# Generated by Django 2.2 on 2021-04-22 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20210419_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='git',
            field=models.URLField(blank=True, max_length=100, null=True, verbose_name='Ссылка'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='self',
            field=models.TextField(blank=True, default='None', max_length=300, null=True, verbose_name='О себе'),
        ),
    ]
