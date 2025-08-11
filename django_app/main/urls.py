"""
URL configuration for main app of StorySmith AI.
Maps URLs to views for story generation functionality.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home page - displays form and handles form submission
    path('', views.home_view, name='home'),
    
    # Results page - displays generated story content
    path('result/', views.result_view, name='result'),
]
