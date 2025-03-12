from django.contrib import admin
from .models import Product, Comment

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    search_fields = ('name',)
    list_filter = ('price', 'quantity')
    ordering = ('price',)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment)

