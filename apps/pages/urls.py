from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('success-stories/', views.success_stories, name='success_stories'),
    path('contact/', views.contact, name='contact'),
]
