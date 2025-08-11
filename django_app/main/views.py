"""
Views for StorySmith AI main app.
Handles the form submission and result display for story generation.
"""

import os
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import StoryInputForm

# Set up logger for this module
logger = logging.getLogger('storysmith')


def home_view(request):
    """
    Home page view that handles both GET (display form) and POST (process form) requests.
    GET: Display the story input form
    POST: Process form data and redirect to results
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
            
            # Store data in session for results page
            request.session['story_data'] = {
                'text_prompt': text_prompt,
                'audio_filename': audio_filename,
            }
            
            # Redirect to results page
            return redirect('result')
        
        else:
            # Form has errors
            logger.warning(f"Form validation failed: {form.errors}")
            messages.error(request, "Please correct the errors below.")
    
    else:
        # GET request - display empty form
        form = StoryInputForm()
    
    return render(request, 'main/input_form.html', {'form': form})


def result_view(request):
    """
    Results page view that displays placeholders for generated content.
    Shows the original user input and placeholders for story, character, and image.
    """
    
    # Get story data from session
    story_data = request.session.get('story_data')
    
    if not story_data:
        # No data in session, redirect to home
        messages.warning(request, "No story data found. Please submit a new request.")
        return redirect('home')
    
    # Log the result page access
    logger.info("User accessed results page")
    
    # Prepare context for template
    context = {
        'text_prompt': story_data['text_prompt'],
        'audio_filename': story_data.get('audio_filename'),
        # Placeholder content for now
        'story_text': 'This is where the generated story will appear. The AI will create an engaging narrative based on your prompt.',
        'character_description': 'Character descriptions and details will be displayed here once the AI processes your request.',
        'scene_image_url': None,  # Will be populated when image generation is integrated
    }
    
    return render(request, 'main/result.html', context)
