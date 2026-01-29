from django.shortcuts import render
from django.utils.translation import get_language
from django.conf import settings
from .models import Office, SocialLink, CompanySettings, HeroSlide
from apps.pages.models import Service
from apps.store.models import Category


def home(request):
    """Homepage view"""
    context = {
        'hero_slides': HeroSlide.objects.filter(is_active=True),
        'offices': Office.objects.filter(is_active=True),
        'services': Service.objects.filter(is_active=True)[:6],
        'categories': Category.objects.filter(is_active=True)[:6],
        'social_links': SocialLink.objects.filter(is_active=True),
    }
    return render(request, 'core/home.html', context)


def set_language(request):
    """Language switching view"""
    from django.http import HttpResponseRedirect
    from django.utils import translation
    
    lang_code = request.GET.get('lang', settings.LANGUAGE_CODE)
    next_url = request.GET.get('next', '/')
    
    response = HttpResponseRedirect(next_url)
    
    if lang_code in [code for code, name in settings.LANGUAGES]:
        if hasattr(request, 'session'):
            request.session['_language'] = lang_code
        
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            lang_code,
            max_age=365 * 24 * 60 * 60,
            domain=settings.SESSION_COOKIE_DOMAIN,
            secure=settings.SESSION_COOKIE_SECURE or False,
            samesite=settings.SESSION_COOKIE_SAMESITE or 'Lax'
        )
        translation.activate(lang_code)
    
    return response


def serviceworker(request):
    """Serve the service worker file"""
    response = render(request, 'serviceworker.js')
    response['Content-Type'] = 'application/javascript'
    response['Service-Worker-Allowed'] = '/'
    return response
