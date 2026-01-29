from django.conf import settings
from django.utils.translation import get_language
from .models import CompanySettings, SocialLink


def global_settings(request):
    """Context processor for global settings available in all templates"""
    
    # Get current language
    current_language = get_language() or settings.LANGUAGE_CODE
    
    # Check if RTL
    is_rtl = current_language in settings.RTL_LANGUAGES
    
    # Get languages
    languages = settings.LANGUAGES
    
    # Get company settings
    try:
        company = CompanySettings.get_settings()
    except:
        company = None
    
    # Get social links
    social_links = SocialLink.objects.filter(is_active=True)
    
    return {
        'COMPANY': company,
        'COMPANY_NAME': settings.COMPANY_NAME,
        'COMPANY_EMAIL': settings.COMPANY_EMAIL,
        'COMPANY_PHONE': settings.COMPANY_PHONE,
        'COMPANY_WHATSAPP': settings.COMPANY_WHATSAPP,
        'SOCIAL_LINKS_SETTINGS': settings.SOCIAL_LINKS,
        'SOCIAL_LINKS': social_links,
        'LANGUAGES': languages,
        'CURRENT_LANGUAGE': current_language,
        'IS_RTL': is_rtl,
        'TEXT_DIR': 'rtl' if is_rtl else 'ltr',
    }
