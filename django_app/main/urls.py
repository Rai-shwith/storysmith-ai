"""
URL configuration for main app of StorySmith AI.
Maps URLs to views for story generation functionality.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home page - displays form and handles form submission
    path('', views.home_view, name='home'),
    
    # Processing page - shows job status with auto-refresh
    path('processing/<uuid:job_id>/', views.processing_view, name='processing'),
    
    # Results page - displays generated story content
    path('result/<uuid:job_id>/', views.result_view, name='result'),
    
    # Retry page - allows user to retry with modified input
    path('retry/<uuid:job_id>/', views.retry_view, name='retry'),
    
    # API endpoint for checking job status
    path('api/job-status/<uuid:job_id>/', views.job_status_api, name='job_status_api'),
]
