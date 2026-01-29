from django.contrib import admin
from .models import Shipment, ShipmentUpdate


class ShipmentUpdateInline(admin.TabularInline):
    model = ShipmentUpdate
    extra = 1
    readonly_fields = ['timestamp']


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = [
        'tracking_number', 'customer_name', 'current_status', 
        'shipping_method', 'destination', 'estimated_delivery', 'created_at'
    ]
    list_filter = ['current_status', 'shipping_method', 'created_at']
    search_fields = ['tracking_number', 'customer_name', 'customer_phone', 'customer_email']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ShipmentUpdateInline]
    
    fieldsets = (
        ('Tracking Info', {
            'fields': ('tracking_number', 'current_status', 'shipping_method')
        }),
        ('Customer Info', {
            'fields': ('user', 'customer_name', 'customer_phone', 'customer_email')
        }),
        ('Shipping Details', {
            'fields': ('origin', 'destination', 'estimated_delivery', 'actual_delivery', 'total_weight', 'total_packages')
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Auto-create status update if status changed
        if change and 'current_status' in form.changed_data:
            ShipmentUpdate.objects.create(
                shipment=obj,
                status=obj.current_status,
                location=obj.destination if obj.current_status in ['arrived', 'delivered'] else obj.origin,
                description=f"Status updated to: {obj.get_current_status_display()}"
            )


@admin.register(ShipmentUpdate)
class ShipmentUpdateAdmin(admin.ModelAdmin):
    list_display = ['shipment', 'status', 'location', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['shipment__tracking_number', 'description']
