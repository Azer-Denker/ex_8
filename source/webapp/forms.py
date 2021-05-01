from django import forms
from .models import Product, Review


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'pic']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'mark', 'status']
