from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    """Product categories"""
    translations = TranslatedFields(
        name=models.CharField(max_length=200, verbose_name="Category Name"),
        description=models.TextField(verbose_name="Description", blank=True),
    )
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        related_name='subcategories',
        null=True, 
        blank=True
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f"Category {self.pk}"
    
    def get_products_count(self):
        return self.products.filter(is_active=True).count()


class Product(TranslatableModel):
    """Products"""
    translations = TranslatedFields(
        name=models.CharField(max_length=300, verbose_name="Product Name"),
        description=models.TextField(verbose_name="Description"),
        specifications=models.TextField(verbose_name="Specifications", blank=True),
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    slug = models.SlugField(unique=True)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="SKU")
    price_rmb = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Price (RMB)")
    min_order_quantity = models.PositiveIntegerField(default=1, verbose_name="Min Order Qty")
    unit = models.CharField(
        max_length=50, 
        default='pieces',
        choices=[
            ('pieces', 'Pieces'),
            ('cartons', 'Cartons'),
            ('sets', 'Sets'),
            ('kg', 'Kilograms'),
            ('meters', 'Meters'),
        ],
        verbose_name="Unit"
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f"Product {self.pk}"
    
    def get_main_image(self):
        """Get the main product image"""
        main_img = self.images.filter(is_main=True).first()
        if main_img:
            return main_img.image
        first_img = self.images.first()
        return first_img.image if first_img else None


class ProductImage(models.Model):
    """Product images"""
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
    
    def __str__(self):
        return f"Image for {self.product}"
    
    def save(self, *args, **kwargs):
        # If this is set as main, unset others
        if self.is_main:
            ProductImage.objects.filter(product=self.product, is_main=True).update(is_main=False)
        super().save(*args, **kwargs)
