from django.db import models
from django.contrib.auth.models import User
from parler.models import TranslatableModel, TranslatedFields


class Shipment(models.Model):
    """Shipment tracking"""
    STATUS_CHOICES = [
        ('order_received', 'Order Received'),
        ('sourcing', 'Sourcing Products'),
        ('quality_check', 'Quality Check'),
        ('packing', 'Packing'),
        ('documentation', 'Documentation & Customs'),
        ('in_transit', 'In Transit'),
        ('arrived', 'Arrived at Destination'),
        ('delivered', 'Delivered'),
    ]
    
    SHIPPING_METHOD_CHOICES = [
        ('air', 'Air Freight'),
        ('sea', 'Sea Freight'),
        ('land', 'Land (Train)'),
        ('express', 'Express Courier'),
    ]
    
    tracking_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='shipments'
    )
    
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=50, blank=True)
    customer_email = models.EmailField(blank=True)
    
    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='order_received')
    shipping_method = models.CharField(max_length=20, choices=SHIPPING_METHOD_CHOICES)
    
    origin = models.CharField(max_length=200, default='China')
    destination = models.CharField(max_length=200)
    
    estimated_delivery = models.DateField(null=True, blank=True)
    actual_delivery = models.DateField(null=True, blank=True)
    
    total_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Weight (kg)")
    total_packages = models.PositiveIntegerField(default=1)
    
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Shipment"
        verbose_name_plural = "Shipments"
    
    def __str__(self):
        return f"{self.tracking_number} - {self.customer_name}"
    
    def get_status_percentage(self):
        """Get progress percentage based on status"""
        status_order = [
            'order_received', 'sourcing', 'quality_check', 'packing',
            'documentation', 'in_transit', 'arrived', 'delivered'
        ]
        try:
            index = status_order.index(self.current_status)
            return int((index + 1) / len(status_order) * 100)
        except ValueError:
            return 0


class ShipmentUpdate(models.Model):
    """Shipment status updates/timeline"""
    shipment = models.ForeignKey(
        Shipment, 
        on_delete=models.CASCADE, 
        related_name='updates'
    )
    status = models.CharField(max_length=20, choices=Shipment.STATUS_CHOICES)
    location = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Shipment Update"
        verbose_name_plural = "Shipment Updates"
    
    def __str__(self):
        return f"{self.shipment.tracking_number} - {self.get_status_display()}"
