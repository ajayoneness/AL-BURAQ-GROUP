from django.db import models
from django.contrib.auth.models import User
from apps.store.models import Product
import uuid


class Order(models.Model):
    """Customer orders"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent_to_whatsapp', 'Sent to WhatsApp'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='orders'
    )
    session_key = models.CharField(max_length=100, blank=True)
    
    # Customer details (for guest checkout)
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField(blank=True)
    customer_phone = models.CharField(max_length=50)
    customer_company = models.CharField(max_length=200, blank=True)
    customer_country = models.CharField(max_length=100, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, verbose_name="Order Notes")
    
    excel_file = models.FileField(upload_to='orders/excel/', blank=True, null=True)
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_items = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Order"
        verbose_name_plural = "Orders"
    
    def __str__(self):
        return f"Order #{self.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Generate unique order number"""
        import datetime
        date_str = datetime.datetime.now().strftime('%Y%m%d')
        unique_id = str(uuid.uuid4().hex)[:6].upper()
        return f"ALB-{date_str}-{unique_id}"
    
    def calculate_totals(self):
        """Recalculate order totals"""
        items = self.items.all()
        self.subtotal = sum(item.get_total() for item in items)
        self.total_items = sum(item.quantity for item in items)
        self.save()


class OrderItem(models.Model):
    """Order line items"""
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.SET_NULL, 
        null=True
    )
    product_name = models.CharField(max_length=300)  # Snapshot of product name
    category_name = models.CharField(max_length=200, blank=True)  # Snapshot
    quantity = models.PositiveIntegerField(default=1)
    unit = models.CharField(max_length=50, default='pieces')
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
    
    def __str__(self):
        return f"{self.quantity}x {self.product_name}"
    
    def get_total(self):
        if self.unit_price is None:
            return 0
        return self.quantity * self.unit_price


class Cart(models.Model):
    """Shopping cart"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='cart'
    )
    session_key = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
    
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart {self.session_key[:8]}"
    
    def get_total(self):
        return sum(item.get_total() for item in self.items.all())
    
    def get_items_count(self):
        return sum(item.quantity for item in self.items.all())
    
    def clear(self):
        self.items.all().delete()


class CartItem(models.Model):
    """Cart line items"""
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'product']
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
    
    def __str__(self):
        return f"{self.quantity}x {self.product}"
    
    def get_total(self):
        return self.quantity * self.product.price_rmb
