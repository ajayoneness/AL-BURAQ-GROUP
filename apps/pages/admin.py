from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import Service, TeamMember, AboutContent, SuccessStory


@admin.register(Service)
class ServiceAdmin(TranslatableAdmin):
    list_display = ['get_title', 'slug', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    prepopulated_fields = {'slug': ('slug',)}
    
    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)
    get_title.short_description = 'Title'


@admin.register(TeamMember)
class TeamMemberAdmin(TranslatableAdmin):
    list_display = ['get_name', 'get_position', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active']
    
    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)
    get_name.short_description = 'Name'
    
    def get_position(self, obj):
        return obj.safe_translation_getter('position', any_language=True)
    get_position.short_description = 'Position'


@admin.register(AboutContent)
class AboutContentAdmin(TranslatableAdmin):
    list_display = ['section_type', 'get_title', 'is_active']
    list_editable = ['is_active']
    list_filter = ['section_type', 'is_active']
    
    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)
    get_title.short_description = 'Title'


@admin.register(SuccessStory)
class SuccessStoryAdmin(TranslatableAdmin):
    list_display = ['get_title', 'get_client', 'order', 'is_active', 'created_at']
    list_editable = ['order', 'is_active']
    list_filter = ['is_active', 'created_at']
    
    def get_title(self, obj):
        return obj.safe_translation_getter('title', any_language=True)
    get_title.short_description = 'Title'
    
    def get_client(self, obj):
        return obj.safe_translation_getter('client_name', any_language=True)
    get_client.short_description = 'Client'
