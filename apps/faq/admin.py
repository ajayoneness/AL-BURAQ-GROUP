from django.contrib import admin
from parler.admin import TranslatableAdmin
from .models import FAQCategory, FAQ


@admin.register(FAQCategory)
class FAQCategoryAdmin(TranslatableAdmin):
    list_display = ['get_name', 'slug', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('slug',)}
    
    def get_name(self, obj):
        return obj.safe_translation_getter('name', any_language=True)
    get_name.short_description = 'Name'


@admin.register(FAQ)
class FAQAdmin(TranslatableAdmin):
    list_display = ['get_question', 'category', 'order', 'is_active', 'updated_at']
    list_editable = ['order', 'is_active']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['translations__question', 'translations__answer']
    
    def get_question(self, obj):
        question = obj.safe_translation_getter('question', any_language=True) or ''
        return question[:80] + '...' if len(question) > 80 else question
    get_question.short_description = 'Question'
