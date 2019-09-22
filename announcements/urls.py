from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='announcements-home'),
    path('about/', views.about, name='announcements-about')
    
]