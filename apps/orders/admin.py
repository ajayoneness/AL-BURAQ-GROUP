from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'category_name', 'unit_price', 'get_total']
    
    def get_total(self, obj):
        return f"¥{obj.get_total()}"
    get_total.short_description = 'Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'customer_name', 'customer_phone', 'status', 'subtotal', 'total_items', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Info', {
            'fields': ('order_number', 'status', 'excel_file')
        }),
        ('Customer Info', {
            'fields': ('user', 'customer_name', 'customer_email', 'customer_phone', 'customer_company', 'customer_country')
        }),
        ('Order Summary', {
            'fields': ('subtotal', 'total_items', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'get_items_count', 'get_total', 'updated_at']
    inlines = [CartItemInline]
    
    def get_items_count(self, obj):
        return obj.get_items_count()
    get_items_count.short_description = 'Items'
    
    def get_total(self, obj):
        return f"¥{obj.get_total()}"
    get_total.short_description = 'Total'
