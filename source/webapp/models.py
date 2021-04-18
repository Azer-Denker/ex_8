from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

STATUS_CHOICES = [
    ('new', 'новый'),
    ('In Progress', 'в процессе'),
    ('Done', 'выполнено')
]


class Tipe(models.Model):
    project_pk = models.ForeignKey('webapp.Project', related_name='projects', on_delete=models.CASCADE,
                                   verbose_name='Проект')
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Заголовок',
                             validators=[MinLengthValidator(5)])
    text = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Текст')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=1, related_name='project',
                               verbose_name='Автор')
    status = models.ForeignKey('webapp.Status', related_name='status', on_delete=models.PROTECT, verbose_name='Статус')
    tags = models.ManyToManyField('webapp.Tag', verbose_name='Теги', blank=True, related_name='tags')
    tipe_team = models.ManyToManyField(User, related_name='tipes', verbose_name='Команда')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    publish_at = models.DateTimeField(verbose_name="Время публикации", blank=True, default=timezone.now)

    def save(self, **kwargs):
        if not self.publish_at:
            if not self.pk:
                self.publish_at = timezone.now()
            else:
                self.publish_at = Tipe.objects.get(pk=self.pk).publish_at
        super().save(**kwargs)

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Status(models.Model):
    name = models.CharField(max_length=15, verbose_name='Статус')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=31, verbose_name='Тег')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.name


class Project(models.Model):
    start_date = models.DateField(null=False, blank=False, verbose_name='Дата начала')
    finish_date = models.DateField(null=True, blank=True, verbose_name='Дата окончания')
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name='Название')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    project_team = models.ManyToManyField(User, related_name='projects', verbose_name='Команда')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "{}. {}".format(self.pk, self.name)

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        permissions = [
            ('add_user_in_project', 'Добавить пользователя в проект')
        ]
