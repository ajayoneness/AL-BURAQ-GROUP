from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product


def category_list(request):
    """Store categories listing"""
    categories = Category.objects.filter(is_active=True, parent__isnull=True)
    
    context = {
        'categories': categories,
    }
    return render(request, 'store/category_list.html', context)


def category_detail(request, slug):
    """Category detail with products"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products = Product.objects.filter(category=category, is_active=True)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': page_obj,
        'subcategories': category.subcategories.filter(is_active=True),
    }
    return render(request, 'store/category_detail.html', context)


def product_detail(request, slug):
    """Individual product detail"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(pk=product.pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    """Product search"""
    query = request.GET.get('q', '')
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(translations__name__icontains=query)
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'query': query,
        'products': page_obj,
    }
    return render(request, 'store/search.html', context)
