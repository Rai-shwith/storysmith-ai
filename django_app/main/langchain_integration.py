"""
LangChain Integration Module for Django
Handles the integration between Django and the LangChain pipeline
"""

import os
import sys
import logging
import threading
import shutil
from pathlib import Path
from django.conf import settings
from django.utils import timezone
from .models import StoryGenerationJob

# Set up logger
logger = logging.getLogger('storysmith')

# Add langchain_app to Python path
LANGCHAIN_APP_PATH = os.path.join(os.path.dirname(settings.BASE_DIR), 'langchain_app')
if LANGCHAIN_APP_PATH not in sys.path:
    sys.path.insert(0, LANGCHAIN_APP_PATH)

def import_langchain_components():
    """Import LangChain components with comprehensive error handling"""
    try:
        # Try to import the enhanced story chain
        from chains.story_chain import create_enhanced_story_chain
        from utils.error_handler import StorySmithError, log_error, log_info
        return create_enhanced_story_chain, StorySmithError, log_error, log_info
    except ImportError as e:
        logger.error(f"Failed to import LangChain components: {e}")
        
        # Create mock classes/functions for testing
        class MockStorySmithError(Exception):
            pass
        
        def mock_log_error(msg):
            logger.error(f"Mock: {msg}")
        
        def mock_log_info(msg):
            logger.info(f"Mock: {msg}")
        
        def mock_create_enhanced_story_chain(generate_images=True):
            class MockChain:
                def invoke(self, input_data):
                    raise MockStorySmithError("LangChain components not available - packages not installed")
            return MockChain()
        
        return mock_create_enhanced_story_chain, MockStorySmithError, mock_log_error, mock_log_info
    except Exception as e:
        logger.error(f"Unexpected error importing LangChain: {e}")
        raise ImportError(f"LangChain integration failed: {e}")

def copy_generated_files_to_media(job_id, langchain_result):
    """
    Copy generated files from langchain_app/outputs to Django media directory
    Returns updated paths relative to MEDIA_ROOT
    """
    media_storysmith_dir = os.path.join(settings.MEDIA_ROOT, 'storysmith')
    os.makedirs(media_storysmith_dir, exist_ok=True)
    
    copied_paths = {}
    
    # Map of result keys to media filenames
    file_mappings = {
        'final_image_path': f'final_image_{job_id}.jpg',
        'character_image_path': f'character_{job_id}.jpg',
        'background_image_path': f'background_{job_id}.jpg'
    }
    
    for result_key, media_filename in file_mappings.items():
        source_path = langchain_result.get(result_key)
        if source_path and os.path.exists(source_path):
            try:
                dest_path = os.path.join(media_storysmith_dir, media_filename)
                shutil.copy2(source_path, dest_path)
                # Store relative path for Django's media handling
                copied_paths[result_key] = f'storysmith/{media_filename}'
                logger.info(f"Copied {source_path} to {dest_path}")
            except Exception as e:
                logger.error(f"Failed to copy {source_path}: {e}")
                copied_paths[result_key] = None
        else:
            copied_paths[result_key] = None
    
    return copied_paths

def process_story_generation(job_id):
    """
    Background thread function to process story generation
    This runs the LangChain pipeline and updates the job status
    """
    job = None
    create_enhanced_story_chain = None
    StorySmithError = Exception  # Default fallback
    log_error = logger.error  # Default fallback
    log_info = logger.info  # Default fallback
    
    try:
        # Get the job
        job = StoryGenerationJob.objects.get(job_id=job_id)
        job.status = 'processing'
        job.started_at = timezone.now()
        job.save()
        
        logger.info(f"Starting story generation for job {job_id}")
        
        # Import LangChain components
        create_enhanced_story_chain, StorySmithError, log_error, log_info = import_langchain_components()
        
        # Create the chain with full pipeline
        chain = create_enhanced_story_chain(generate_images=True)
        
        # Execute the pipeline
        result = chain.invoke({"topic": job.text_prompt})
        
        # Copy generated files to media directory
        copied_paths = copy_generated_files_to_media(job_id, result)
        
        # Update job with results
        job.story_text = result.get('story', '')
        job.character_description = result.get('character_description', '')
        job.background_description = result.get('background_description', '')
        job.detected_style = result.get('detected_style', '')
        
        # Update image paths
        job.final_image_path = copied_paths.get('final_image_path')
        job.character_image_path = copied_paths.get('character_image_path')
        job.background_image_path = copied_paths.get('background_image_path')
        
        job.status = 'completed'
        job.completed_at = timezone.now()
        job.error_message = None
        job.save()
        
        logger.info(f"Story generation completed for job {job_id}")
        
    except Exception as e:
        # Handle all errors (including StorySmithError and ImportError)
        error_msg = f"Story generation error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        
        if job:
            job.status = 'failed'
            job.error_message = error_msg
            job.completed_at = timezone.now()
            job.save()
        
        # Log additional context for debugging
        if "LangChain components not available" in str(e):
            logger.info("This error is expected when LangChain packages are not installed")
        elif "circular import" in str(e):
            logger.info("This error indicates a circular import in the LangChain code")
        elif "cannot import" in str(e):
            logger.info("This error indicates missing Python packages")

def start_story_generation_async(text_prompt, audio_filename=None):
    """
    Start asynchronous story generation
    Returns the job instance
    """
    # Create new job
    job = StoryGenerationJob.objects.create(
        text_prompt=text_prompt,
        audio_filename=audio_filename,
        status='pending'
    )
    
    # Start background thread
    thread = threading.Thread(
        target=process_story_generation,
        args=(job.job_id,),
        daemon=True  # Thread dies when main program exits
    )
    thread.start()
    
    logger.info(f"Started async story generation for job {job.job_id}")
    return job

def get_job_status(job_id):
    """Get current status and results of a job"""
    try:
        job = StoryGenerationJob.objects.get(job_id=job_id)
        return {
            'status': job.status,
            'job': job,
            'exists': True
        }
    except StoryGenerationJob.DoesNotExist:
        return {
            'status': 'not_found',
            'job': None,
            'exists': False
        }
