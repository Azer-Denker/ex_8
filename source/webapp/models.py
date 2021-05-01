from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

CATEGORY_CHOICES = (
    ('Other', 'Разное'),
    ('Food', 'Продукты питания'),
    ('Household', 'Хозяйство'),
    ('Toys', 'Игрушки'),
    ('Appliances', 'Бытовая Техника')
)


class Product(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name='Название')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Категория')
    description = models.TextField(max_length=3000, null=True, blank=True, verbose_name='Описание')
    pic = models.ImageField(null=True, blank=True, upload_to='product_pic', verbose_name='Картинка')

    def __str__(self):
        return "{}. {}".format(self.pk, self.name)

    def get_mark(self):
        total = 0
        reviews = Review.objects.filter(product=self.pk)
        if reviews.count():
            for x in reviews.filter(status=True):
                total += int(x.mark)
            try:
                total = total / reviews.filter(status=True).count()
            except ZeroDivisionError:
                total = 0
        return round(total, 1)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Review(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=1, related_name='product',
                               verbose_name='Автор')
    product = models.ForeignKey('webapp.Product', related_name='product_review', on_delete=models.CASCADE,
                                verbose_name='Товар')
    text = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Текст отзыва')
    mark = models.IntegerField(verbose_name='Оценка', validators=[MinValueValidator(0), MaxValueValidator(5)])
    status = models.BooleanField(default=False, verbose_name="Статус")
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Время создания')
    updated_at = models.DateTimeField(default=timezone.now, verbose_name='Время изменения')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
