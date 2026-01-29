from django.shortcuts import render, get_object_or_404
from .models import Service, TeamMember, AboutContent, SuccessStory
from apps.core.models import Office


def about(request):
    """About Us page"""
    context = {
        'about_contents': AboutContent.objects.filter(is_active=True),
        'team_members': TeamMember.objects.filter(is_active=True),
        'offices': Office.objects.filter(is_active=True),
    }
    return render(request, 'pages/about.html', context)


def services(request):
    """Services listing page"""
    context = {
        'services': Service.objects.filter(is_active=True),
    }
    return render(request, 'pages/services.html', context)


def service_detail(request, slug):
    """Individual service detail page"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    other_services = Service.objects.filter(is_active=True).exclude(pk=service.pk)[:4]
    
    context = {
        'service': service,
        'other_services': other_services,
    }
    return render(request, 'pages/service_detail.html', context)


def success_stories(request):
    """Success stories page"""
    context = {
        'stories': SuccessStory.objects.filter(is_active=True),
    }
    return render(request, 'pages/success_stories.html', context)


def contact(request):
    """Contact page"""
    context = {
        'offices': Office.objects.filter(is_active=True),
    }
    return render(request, 'pages/contact.html', context)
