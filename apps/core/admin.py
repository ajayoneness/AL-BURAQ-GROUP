from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Office, SocialLink, CompanySettings, HeroSlide


@admin.register(Office)
class OfficeAdmin(TranslatableAdmin):
    list_display = ['get_name', 'phone', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    
    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)
    get_name.short_description = 'Name'


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ['platform', 'url', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['platform', 'is_active']


@admin.register(CompanySettings)
class CompanySettingsAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'email', 'phone']
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not CompanySettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSlide)
class HeroSlideAdmin(TranslatableAdmin):
    list_display = ['get_title', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    
    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)
    get_title.short_description = 'Title'
