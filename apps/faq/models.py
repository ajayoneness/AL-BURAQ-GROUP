from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class FAQCategory(TranslatableModel):
    """FAQ categories"""
    translations = TranslatedFields(
        name=models.CharField(max_length=200, verbose_name="Category Name"),
    )
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "FAQ Category"
        verbose_name_plural = "FAQ Categories"
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f"Category {self.pk}"


class FAQ(TranslatableModel):
    """Frequently Asked Questions"""
    translations = TranslatedFields(
        question=models.CharField(max_length=500, verbose_name="Question"),
        answer=models.TextField(verbose_name="Answer"),
    )
    category = models.ForeignKey(
        FAQCategory, 
        on_delete=models.CASCADE, 
        related_name='faqs',
        null=True,
        blank=True
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
    
    def __str__(self):
        return self.safe_translation_getter('question', any_language=True) or f"FAQ {self.pk}"
