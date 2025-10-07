from django.contrib import admin
from .models import Product, Category

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_per_page = 10

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 10


