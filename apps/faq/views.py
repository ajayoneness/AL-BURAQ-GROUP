from django.shortcuts import render
from .models import FAQCategory, FAQ


def faq_list(request):
    """FAQ listing page with accordion"""
    categories = FAQCategory.objects.filter(is_active=True).prefetch_related('faqs')
    uncategorized_faqs = FAQ.objects.filter(is_active=True, category__isnull=True)
    
    context = {
        'categories': categories,
        'uncategorized_faqs': uncategorized_faqs,
    }
    return render(request, 'faq/faq_list.html', context)
