from django.contrib import admin
from .models import Product, Media, Transaction, SalesOrder, SalesOrderItem, Contact, Support


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


class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    readonly_fields = ('product', 'price')  # Make product and price read-only
    extra = 0  # Set the number of extra inline forms to display (0 for none)


class SalesOrderAdmin(admin.ModelAdmin):
    inlines = [SalesOrderItemInline]
    list_display = ('user', 'number', 'date', 'items_total', 'order_total')
    readonly_fields = ('user', 'number', 'date')  # Make user, number, and date read-only


admin.site.register(SalesOrder, SalesOrderAdmin)


# Register the Transaction model with custom admin settings
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'name')
    list_filter = ('name', 'email')
    search_fields = ('reference_number', 'email')


# Register the Transaction model with custom admin settings
@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ('reference_number', 'name')
    list_filter = ('name', 'email')
    search_fields = ('reference_number', 'email')
