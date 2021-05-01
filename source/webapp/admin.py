from django.contrib import admin
from webapp.models import Product, Review


class StatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    fields = ['name']


admin.site.register(Product)
admin.site.register(Review)
