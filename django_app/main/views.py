"""
Views for StorySmith AI main app.
Handles the form submission and result display for story generation.
"""

import os
import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.urls import reverse
from .forms import StoryInputForm
from .models import StoryGenerationJob
from .langchain_integration import start_story_generation_async, get_job_status

# Set up logger for this module
logger = logging.getLogger('storysmith')


def home_view(request):
    """
    Home page view that handles both GET (display form) and POST (process form) requests.
    GET: Display the story input form
    POST: Process form data and start async story generation
    """
    
    if request.method == 'POST':
        form = StoryInputForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Get cleaned data
            text_prompt = form.cleaned_data['text_prompt']
            audio_file = form.cleaned_data.get('audio_file')
            
            # Log the user input
            logger.info(f"New story request - Text prompt: {text_prompt[:50]}...")
            
            # Handle audio file if provided
            audio_filename = None
            if audio_file:
                # Create media directory if it doesn't exist
                media_audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio_uploads')
                os.makedirs(media_audio_dir, exist_ok=True)
                
                # Save the audio file
                audio_filename = default_storage.save(
                    f'audio_uploads/{audio_file.name}',
                    ContentFile(audio_file.read())
                )
                
                logger.info(f"Audio received and saved: {audio_filename}")
                print("Audio received")  # Console output as requested
            
            try:
                # Start async story generation
                job = start_story_generation_async(text_prompt, audio_filename)
                
                # Store job_id in session
                request.session['current_job_id'] = str(job.job_id)
                
                # Redirect to processing page
                return redirect('processing', job_id=job.job_id)
                
            except Exception as e:
                logger.error(f"Failed to start story generation: {e}")
                messages.error(request, "Failed to start story generation. Please try again.")
                # Return form with error
                return render(request, 'main/input_form.html', {
                    'form': form,
                    'error': "Failed to start story generation. Please check that the LangChain app is properly configured."
                })
        
        else:
            # Form has errors
            logger.warning(f"Form validation failed: {form.errors}")
            messages.error(request, "Please correct the errors below.")
    
    else:
        # GET request - display empty form
        form = StoryInputForm()
    
    return render(request, 'main/input_form.html', {'form': form})


def processing_view(request, job_id):
    """
    Processing page that shows job status and auto-refreshes
    """
    job_status = get_job_status(job_id)
    
    if not job_status['exists']:
        messages.error(request, "Job not found.")
        return redirect('home')
    
    job = job_status['job']
    
    # Check if job is completed
    if job.status == 'completed':
        return redirect('result', job_id=job_id)
    
    context = {
        'job': job,
        'job_id': job_id,
        'refresh_url': reverse('processing', kwargs={'job_id': job_id}),
        'result_url': reverse('result', kwargs={'job_id': job_id}),
    }
    
    return render(request, 'main/processing.html', context)


def job_status_api(request, job_id):
    """
    API endpoint to check job status (for AJAX polling)
    """
    job_status = get_job_status(job_id)
    
    if not job_status['exists']:
        return JsonResponse({'status': 'not_found'})
    
    job = job_status['job']
    response_data = {
        'status': job.status,
        'created_at': job.created_at.isoformat() if job.created_at else None,
        'started_at': job.started_at.isoformat() if job.started_at else None,
        'completed_at': job.completed_at.isoformat() if job.completed_at else None,
        'error_message': job.error_message,
    }
    
    if job.status == 'completed':
        response_data['redirect_url'] = reverse('result', kwargs={'job_id': job_id})
    
    return JsonResponse(response_data)


def result_view(request, job_id):
    """
    Results page view that displays the generated story and images
    """
    job_status = get_job_status(job_id)
    
    if not job_status['exists']:
        messages.error(request, "Job not found.")
        return redirect('home')
    
    job = job_status['job']
    
    if job.status != 'completed':
        # Job not completed, redirect to processing page
        return redirect('processing', job_id=job_id)
    
    # Log the result page access
    logger.info(f"User accessed results for job {job_id}")
    
    # Prepare context for template
    context = {
        'job': job,
        'text_prompt': job.text_prompt,
        'audio_filename': job.audio_filename,
        'story_text': job.story_text,
        'character_description': job.character_description,
        'background_description': job.background_description,
        'detected_style': job.detected_style,
        'final_image_url': job.final_image_path,
        'character_image_url': job.character_image_path,
        'background_image_url': job.background_image_path,
        'retry_url': reverse('retry', kwargs={'job_id': job_id}),
    }
    
    return render(request, 'main/result.html', context)


def retry_view(request, job_id):
    """
    Retry view that pre-populates the form with previous job data
    """
    job_status = get_job_status(job_id)
    
    if not job_status['exists']:
        messages.error(request, "Original job not found.")
        return redirect('home')
    
    job = job_status['job']
    
    if request.method == 'POST':
        form = StoryInputForm(request.POST, request.FILES)
        
        if form.is_valid():
            # Get cleaned data
            text_prompt = form.cleaned_data['text_prompt']
            audio_file = form.cleaned_data.get('audio_file')
            
            # Handle audio file if provided
            audio_filename = None
            if audio_file:
                media_audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio_uploads')
                os.makedirs(media_audio_dir, exist_ok=True)
                
                audio_filename = default_storage.save(
                    f'audio_uploads/{audio_file.name}',
                    ContentFile(audio_file.read())
                )
            
            try:
                # Start new async story generation
                new_job = start_story_generation_async(text_prompt, audio_filename)
                
                # Store new job_id in session
                request.session['current_job_id'] = str(new_job.job_id)
                
                # Redirect to processing page for new job
                return redirect('processing', job_id=new_job.job_id)
                
            except Exception as e:
                logger.error(f"Failed to start retry story generation: {e}")
                messages.error(request, "Failed to start story generation. Please try again.")
    
    else:
        # GET request - pre-populate form with previous job data
        initial_data = {
            'text_prompt': job.text_prompt,
        }
        form = StoryInputForm(initial=initial_data)
    
    context = {
        'form': form,
        'original_job': job,
        'is_retry': True,
    }
    
    return render(request, 'main/input_form.html', context)
