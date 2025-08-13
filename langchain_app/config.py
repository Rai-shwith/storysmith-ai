"""
Configuration file for StorySmith AI
Contains all constants, model paths, and environment variables
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Hugging Face Configuration - Support both token variable names
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN") or os.getenv("HUGGINGFACEHUB_API_TOKEN")
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models"

# Model Configuration - Using models available on HuggingFace Inference API
# Using GPT-2 as it's always available and works with text generation API
TEXT_GENERATION_MODEL = "gpt2"  # Always available, reliable for text generation
IMAGE_GENERATION_MODEL = "runwayml/stable-diffusion-v1-5"  # Can switch to local model

# Alternative text models (verified to work with HF Inference API for text generation)
ALTERNATIVE_TEXT_MODELS = [
    "gpt2",                         # Classic GPT-2 (always available as fallback)
    "gpt2-medium",                  # Larger GPT-2 version
    "distilgpt2",                   # Smaller, faster version of GPT-2
    "microsoft/DialoGPT-medium",    # Conversational, good for stories
    "microsoft/DialoGPT-small",     # Smaller conversational model
    "EleutherAI/gpt-neo-125M",      # Open-source GPT alternative
]

ALTERNATIVE_IMAGE_MODELS = [
    "stabilityai/stable-diffusion-2-1",
    "CompVis/stable-diffusion-v1-4",
    "runwayml/stable-diffusion-v1-5"
]

# Local Model Paths (for GPU usage)
LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", "./models")
USE_LOCAL_MODELS = os.getenv("USE_LOCAL_MODELS", "false").lower() == "true"

# Image Configuration
IMAGE_SIZE = (512, 512)  # Default image size
CHARACTER_POSITION = "center"  # Position for character placement
BACKGROUND_REMOVE_THRESHOLD = 240  # White background removal threshold (0-255)

# Output Configuration
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./outputs")
TEMP_DIR = os.getenv("TEMP_DIR", "./temp")

# API Configuration
API_TIMEOUT = 60  # seconds
MAX_RETRIES = 3
RATE_LIMIT_WAIT = 2  # seconds between requests

# Story Generation Prompts - Optimized for GPT-2 style continuation
STORY_PROMPT_TEMPLATE = """
Topic: {topic}

STORY: Once upon a time, in a magical place, there lived a character who would embark on an incredible adventure. The story begins when
"""

# Image Prompt Templates
CHARACTER_PROMPT_TEMPLATE = """
{character_description}, full body shot, isolated on pure white background, 
png style, no background, clean edges, high quality, detailed, 
{style_modifier}
"""

BACKGROUND_PROMPT_TEMPLATE = """
{background_description}, detailed environment, 
atmospheric lighting, high quality, cinematic, 
{style_modifier}
"""

# Style modifiers based on story genre/mood
STYLE_MODIFIERS = {
    "fantasy": "fantasy art style, magical atmosphere",
    "sci-fi": "sci-fi concept art, futuristic",
    "horror": "dark atmosphere, gothic style",
    "romance": "soft lighting, romantic atmosphere",
    "adventure": "epic scale, dramatic lighting",
    "mystery": "noir style, mysterious atmosphere",
    "default": "professional illustration style"
}

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "storysmith.log")

# Create necessary directories
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
if USE_LOCAL_MODELS:
    os.makedirs(LOCAL_MODEL_PATH, exist_ok=True)
