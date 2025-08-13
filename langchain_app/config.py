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

# Model Configuration - Using local models for text generation
# Using Phi-3-mini for high-quality text generation
TEXT_GENERATION_MODEL = "microsoft/Phi-3-mini-4k-instruct"  # Primary model for local execution
IMAGE_GENERATION_MODEL = "stabilityai/sdxl-base-1.0"  # High-quality SDXL for local execution

# Alternative text models (fallback options for local execution)
ALTERNATIVE_TEXT_MODELS = [
    "microsoft/Phi-3-mini-4k-instruct",  # Primary choice - excellent for instruction following
    "gpt2",                         # Classic GPT-2 (lightweight fallback)
    "gpt2-medium",                  # Larger GPT-2 version
    "distilgpt2",                   # Smaller, faster version of GPT-2
    "microsoft/DialoGPT-medium",    # Conversational, good for stories
    "microsoft/DialoGPT-small",     # Smaller conversational model
    "EleutherAI/gpt-neo-125M",      # Open-source GPT alternative
]

ALTERNATIVE_IMAGE_MODELS = [
    "stabilityai/sdxl-base-1.0",        # Primary choice - highest quality
    "stabilityai/stable-diffusion-2-1",
    "CompVis/stable-diffusion-v1-4",
    "runwayml/stable-diffusion-v1-5"
]

# Local Model Paths (for local execution)
LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", "./models")
USE_LOCAL_MODELS = os.getenv("USE_LOCAL_MODELS", "true").lower() == "true"  # Default to local execution

# Image Configuration
IMAGE_SIZE = (1024, 1024)  # SDXL native resolution for best quality
CHARACTER_POSITION = "center"  # Position for character placement
BACKGROUND_REMOVE_THRESHOLD = 240  # White background removal threshold (0-255)

# Output Configuration
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./outputs")
TEMP_DIR = os.getenv("TEMP_DIR", "./temp")

# API Configuration
API_TIMEOUT = 60  # seconds
MAX_RETRIES = 3
RATE_LIMIT_WAIT = 2  # seconds between requests

# Story Generation Prompts - Optimized for Phi-3-mini instruction following
STORY_PROMPT_TEMPLATE = """
<|system|>You are a creative storyteller who writes engaging and imaginative stories.<|end|>
<|user|>Write a complete short story about: {topic}

The story should be engaging, creative, and approximately 200-300 words. Include interesting characters, a clear beginning, middle, and end.<|end|>
<|assistant|>
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
