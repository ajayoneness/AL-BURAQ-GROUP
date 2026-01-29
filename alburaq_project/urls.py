"""
URL configuration for alburaq_project project.
AL BURAQ GROUP - International Trade & Logistics
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

# Main URLs (language-prefixed)
urlpatterns += [
    path('', include('apps.core.urls')),
    path('', include('apps.pages.urls')),
    path('faq/', include('apps.faq.urls')),
    path('store/', include('apps.store.urls')),
    path('orders/', include('apps.orders.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('tracking/', include('apps.tracking.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Admin customization
admin.site.site_header = "AL BURAQ GROUP Admin"
admin.site.site_title = "AL BURAQ Admin"
admin.site.index_title = "Welcome to AL BURAQ GROUP Administration"
