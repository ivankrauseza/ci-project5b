from django.contrib import admin
from .models import Product, Media, Transaction


class MediaInline(admin.TabularInline):
    model = Media
    extra = 1  # Number of extra media forms to display


# Register the Product model with custom admin settings
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [MediaInline]
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
            'classes': ('collapse',)
        })
    )


# Register the Transaction model with custom admin settings
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'type', 'date_added')
    list_filter = ('type', 'date_added')
    search_fields = ('user__username', 'product__name')
