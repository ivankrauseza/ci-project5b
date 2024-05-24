from django.contrib import admin
from .models import Product, Media, Transaction, SalesOrder, SalesOrderItem, Contact, Support, Profile


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
    readonly_fields = ['sales_order', 'product', 'quantity', 'price']
    can_delete = False
    extra = 0  # Do not display any extra blank forms


class SalesOrderAdmin(admin.ModelAdmin):
    readonly_fields = [
        'user', 'date', 'number', 'billing_name', 'billing_address', 'billing_phone',
        'shipping_name', 'shipping_address', 'shipping_phone', 'items_total', 'delivery_amount',
        'vat_amount', 'order_total'
    ]
    inlines = [SalesOrderItemInline]
    list_display = ['number', 'user', 'date', 'order_total']
    search_fields = ['number', 'user__username']
    list_filter = ['date']


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


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'stripe_id', 'billing_name', 'shipping_name')
    search_fields = ('user__username', 'billing_name', 'shipping_name')
