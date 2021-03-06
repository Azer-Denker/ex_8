# Generated by Django 2.2 on 2021-04-19 10:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='user_pics', verbose_name='Аватара')),
                ('self', models.TextField(blank=True, default=None, max_length=2000, null=True, verbose_name='О себе')),
                ('git', models.URLField(blank=True, max_length=150, null=True, verbose_name='Гитхаб ауукант')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
                'permissions': {('can_watch_users', 'может видеть список пользователей')},
            },
        ),
    ]
