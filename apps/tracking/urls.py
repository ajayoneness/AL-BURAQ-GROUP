from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('', views.tracking_page, name='tracking'),
    path('ajax/', views.track_ajax, name='track_ajax'),
]
