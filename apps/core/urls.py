from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('set-language/', views.set_language, name='set_language'),
    path('serviceworker.js', views.serviceworker, name='serviceworker'),
]
