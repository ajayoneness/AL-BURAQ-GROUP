from django.db import models
from parler.models import TranslatableModel, TranslatedFields


class Office(TranslatableModel):
    """Company office locations"""
    translations = TranslatedFields(
        name=models.CharField(max_length=200, verbose_name="Office Name"),
        address=models.TextField(verbose_name="Address"),
        location_tag=models.CharField(max_length=100, verbose_name="Location Tag", blank=True)
    )
    phone = models.CharField(max_length=50, verbose_name="Phone Number")
    icon = models.CharField(max_length=50, default='fa-building', verbose_name="Icon Class")
    image = models.ImageField(upload_to='offices/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Office"
        verbose_name_plural = "Offices"
    
    def __str__(self):
        return self.safe_translation_getter('name', any_language=True) or f"Office {self.pk}"


class SocialLink(models.Model):
    """Company social media links"""
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('twitter', 'Twitter/X'),
        ('linkedin', 'LinkedIn'),
        ('whatsapp', 'WhatsApp'),
    ]
    
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    url = models.URLField(verbose_name="URL")
    icon = models.CharField(max_length=50, verbose_name="Icon Class")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Social Link"
        verbose_name_plural = "Social Links"
    
    def __str__(self):
        return self.get_platform_display()


class CompanySettings(models.Model):
    """Singleton model for company settings"""
    company_name = models.CharField(max_length=200, default="AL BURAQ GROUP")
    email = models.EmailField(default="alburaqgroupcn@gmail.com")
    phone = models.CharField(max_length=50, default="+8619557959148")
    whatsapp_number = models.CharField(max_length=50, default="+8619557959148")
    logo = models.ImageField(upload_to='branding/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Company Settings"
        verbose_name_plural = "Company Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
    
    def __str__(self):
        return self.company_name


class HeroSlide(TranslatableModel):
    """Hero section slides for homepage"""
    translations = TranslatedFields(
        title=models.CharField(max_length=200, verbose_name="Title"),
        subtitle=models.TextField(verbose_name="Subtitle", blank=True),
        button_text=models.CharField(max_length=100, blank=True, verbose_name="Button Text"),
    )
    button_url = models.CharField(max_length=200, blank=True)
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Hero Slide"
        verbose_name_plural = "Hero Slides"
    
    def __str__(self):
        return self.safe_translation_getter('title', any_language=True) or f"Slide {self.pk}"
