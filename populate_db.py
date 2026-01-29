import os
import django
import random
from datetime import timedelta
from django.utils import timezone
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alburaq_project.settings')
django.setup()

from apps.store.models import Category, Product
from apps.pages.models import Service
from apps.core.models import Office
from apps.faq.models import FAQ

def populate():
    print("Populating database with demo data...")
    
    # 1. Categories
    categories_data = [
        ('Electronics', 'Latest gadgets and electronic components directly from Shenzhen.', 'fas fa-plug'),
        ('Home & Garden', 'Furniture, decor, and garden tools for modern living.', 'fas fa-couch'),
        ('Fashion', 'Trendy clothing, accessories, and footwear.', 'fas fa-tshirt'),
        ('Machinery', 'Industrial machinery and equipment for manufacturing.', 'fas fa-cogs'),
        ('Beauty', 'Cosmetics and personal care products.', 'fas fa-magic'),
        ('Toys', 'Safe and fun toys for all ages.', 'fas fa-gamepad'),
    ]
    
    categories = []
    for name, desc, icon in categories_data:
        cat, created = Category.objects.get_or_create(
            slug=name.lower().replace(' ', '-').replace('&', 'and'),
            defaults={'name': name, 'description': desc}
        )
        categories.append(cat)
        if created:
            print(f"Created Category: {name}")
    
    # 2. Products
    products_data = [
        ('Smartphone X1', 0, 299.99),
        ('Wireless Earbuds', 0, 49.99),
        ('Smart Watch Pro', 0, 89.99),
        ('Garden Sofa Set', 1, 450.00),
        ('Modern Lamp', 1, 35.00),
        ('Summer Dress', 2, 25.00),
        ('Running Shoes', 2, 45.00),
        ('Leather Bag', 2, 60.00),
        ('CNC Machine', 3, 5000.00),
        ('Lipstick Set', 4, 15.00),
        ('Building Blocks', 5, 20.00),
    ]
    
    for name, cat_idx, price in products_data:
        slug = name.lower().replace(' ', '-')
        if not Product.objects.filter(slug=slug).exists():
            Product.objects.create(
                category=categories[cat_idx],
                name=name,
                slug=slug,
                description=f"High quality {name} available for wholesale. Minimum order quantity applies.",
                price_rmb=price * 7, # Approx exchange
                min_order_quantity=random.randint(10, 100),
                is_active=True,
                is_featured=random.choice([True, False])
            )
            print(f"Created Product: {name}")

    # 3. FAQs
    from apps.faq.models import FAQCategory
    shipping_cat, _ = FAQCategory.objects.get_or_create(
        slug='shipping', 
        defaults={'name': 'Shipping & Delivery', 'is_active': True}
    )

    faqs_data = [
        ('How long does shipping take?', 'Air shipping usually takes 3-7 days, while sea shipping takes 20-40 days depending on the destination.'),
        ('Do you offer samples?', 'Yes, we can arrange samples from manufacturers before you place a bulk order.'),
        ('What is your MOQ?', 'MOQ depends on the product. Generally 100-500 units for customized products.'),
        ('Can you handle customs clearance?', 'Yes, we provide full DDP (Delivered Duty Paid) services for many countries.'),
    ]
    
    for q, a in faqs_data:
        if not FAQ.objects.filter(translations__question=q).exists():
            FAQ.objects.create(
                question=q,
                answer=a,
                is_active=True, 
                category=shipping_cat
            )
            print(f"Created FAQ: {q}")

    # 4. Offices (Ensure active)
    Office.objects.update(is_active=True)
    
    print("Done! Database populated.")

if __name__ == "__main__":
    populate()
