from django.contrib import admin
from .models import Product


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'stock', 'brand', 'collection', 'type', 'created', 'updated', 'blocked')
    list_filter = ('brand', 'collection', 'type', 'created', 'updated', 'blocked')
    search_fields = ['name', 'sku', 'brand']
    readonly_fields = ('created', 'updated')
    fieldsets = (
        (None, {
            'fields': ('sku', 'name', 'blurb', 'desc', 'stock', 'price', 'brand', 'collection', 'type')
        }),
        ('Status', {
            'fields': ('created', 'updated', 'blocked'),
            'classes': ('collapse', )
        })
    )
