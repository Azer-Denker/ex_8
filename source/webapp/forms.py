from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
from django.utils.deconstruct import deconstructible

from .models import STATUS_CHOICES, Tipe, Project

default_status = STATUS_CHOICES[0][0]

BROWSER_DATETIME_FORMAT = '%d.%m.%Y %H:%M'


class XDatepickerWidget(forms.TextInput):
    template_name = 'widgets/xdatepicker_widget.html'


def at_least_10(string):
    if len(string) < 10:
        raise ValidationError('This value is too short!')


@deconstructible
class MinLengthValidator(BaseValidator):
    message = 'Value "%(value)s" has length of %(show_value)d! It should be at least %(limit_value)d symbols long!'
    code = 'too_short'

    def compare(self, value, limit):
        return value < limit

    def clean(self, value):
        return len(value)


class TipeForm(forms.ModelForm):
    publish_at = forms.DateTimeField(required=False, label='Время публикации',
                                     input_formats=['%Y-%m-%d', BROWSER_DATETIME_FORMAT,
                                                    '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M',
                                                    '%Y-%m-%d %H:%M:%S'],
                                     widget=XDatepickerWidget)

    class Meta:
        model = Tipe
        fields = ['title', 'text', 'author', 'status', 'publish_at', 'tags']
        widgets = {'tags': forms.CheckboxSelectMultiple}

    def clean(self):
        cleaned_data = super().clean()
        errors = []
        text = cleaned_data.get('text')
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        if text and title and text == title:
            errors.append(ValidationError("Text of the tipe should not duplicate it's title!"))
        if title and author and title == author:
            errors.append(ValidationError("You should not write about yourself! It's a spam!"))
        if errors:
            raise ValidationError(errors)
        return cleaned_data


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['start_date', 'finish_date', 'name', 'description']


class ProjectDeleteForm(forms.Form):
    title = forms.CharField(max_length=120, required=True, label='Введите название Проекта, чтобы удалить её')
