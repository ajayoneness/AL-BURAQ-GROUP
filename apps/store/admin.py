from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Category, Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['get_name', 'slug', 'parent', 'get_products_count', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'parent']
    search_fields = ['translations__name']
    prepopulated_fields = {'slug': ('slug',)}
    
    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)
    get_name.short_description = 'Name'
    
    def get_products_count(self, obj):
        return obj.get_products_count()
    get_products_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['get_name', 'category', 'price_rmb', 'unit', 'min_order_quantity', 'is_active', 'is_featured']
    list_editable = ['is_active', 'is_featured']
    list_filter = ['category', 'is_active', 'is_featured', 'unit']
    search_fields = ['translations__name', 'sku']
    prepopulated_fields = {'slug': ('slug',)}
    inlines = [ProductImageInline]
    
    def get_name(self, obj):
        name = obj.safe_translation_getter('name', any_language=True) or ''
        return name[:50] + '...' if len(name) > 50 else name
    get_name.short_description = 'Name'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_main', 'order']
    list_editable = ['is_main', 'order']
    list_filter = ['is_main']
