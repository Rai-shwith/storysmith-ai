from django.db import models
import uuid
from django.utils import timezone

class StoryGenerationJob(models.Model):
    """Model to track story generation jobs"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    job_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    text_prompt = models.TextField()
    audio_filename = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Generated content
    story_text = models.TextField(blank=True, null=True)
    character_description = models.TextField(blank=True, null=True)
    background_description = models.TextField(blank=True, null=True)
    detected_style = models.CharField(max_length=100, blank=True, null=True)
    
    # Image paths (relative to MEDIA_ROOT)
    final_image_path = models.CharField(max_length=500, blank=True, null=True)
    character_image_path = models.CharField(max_length=500, blank=True, null=True)
    background_image_path = models.CharField(max_length=500, blank=True, null=True)
    
    # Error handling
    error_message = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    started_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"Job {self.job_id} - {self.status}"
