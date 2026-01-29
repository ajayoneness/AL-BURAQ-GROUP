from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Service(TranslatableModel):
    """Company services"""
    translations = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name="Title"),
        short_description=models.TextField(verbose_name="Short Description"),
        full_description=models.TextField(verbose_name="Full Description", blank=True),
    )
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=100, default='fa-shipping-fast', verbose_name="Icon Class")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Service"
        verbose_name_plural = "Services"
    
    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or f"Service {self.pk}"


class TeamMember(TranslatableModel):
    """Team members for About page"""
    translations = TranslatedFields(
        name=models.CharField(max_length=200, verbose_name="Name"),
        position=models.CharField(max_length=200, verbose_name="Position"),
        bio=models.TextField(verbose_name="Biography", blank=True),
    )
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f"Member {self.pk}"


class AboutContent(TranslatableModel):
    """About page content sections"""
    translations = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name="Section Title"),
        content=models.TextField(verbose_name="Content"),
    )
    section_type = models.CharField(
        max_length=50,
        choices=[
            ('intro', 'Introduction'),
            ('history', 'History'),
            ('vision', 'Vision'),
            ('mission', 'Mission'),
            ('values', 'Values'),
        ],
        unique=True
    )
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "About Content"
        verbose_name_plural = "About Contents"
    
    def __str__(self):
        return self.get_section_type_display()


class SuccessStory(TranslatableModel):
    """Success stories/case studies"""
    translations = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name="Title"),
        client_name=models.CharField(max_length=200, verbose_name="Client Name"),
        description=models.TextField(verbose_name="Description"),
    )
    image = models.ImageField(upload_to='success_stories/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Success Story"
        verbose_name_plural = "Success Stories"
    
    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or f"Story {self.pk}"
