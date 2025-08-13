"""
Image merging utilities using Pillow
Handles background removal and character placement
"""

import os
import sys
import requests
import time
from PIL import Image, ImageDraw
from typing import Tuple, Optional
from io import BytesIO

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    HUGGINGFACE_API_TOKEN,
    HUGGINGFACE_API_URL,
    IMAGE_GENERATION_MODEL,
    IMAGE_SIZE,
    BACKGROUND_REMOVE_THRESHOLD,
    API_TIMEOUT,
    MAX_RETRIES,
    RATE_LIMIT_WAIT,
    OUTPUT_DIR,
    TEMP_DIR,
    USE_LOCAL_MODELS
)
from utils.error_handler import log_error, log_info, ImageProcessingError


def generate_image_from_prompt(prompt: str, filename: str) -> str:
    """Generate image using local models or Hugging Face API"""
    try:
        if USE_LOCAL_MODELS:
            return _generate_image_local(prompt, filename)
        else:
            return _generate_image_api(prompt, filename)
        
    except Exception as e:
        log_error(f"Error generating image {filename}", e)
        raise ImageProcessingError(f"Image generation failed: {e}")


def _generate_image_local(prompt: str, filename: str) -> str:
    """Generate image using local diffusion model"""
    try:
        from diffusers import StableDiffusionXLPipeline
        import torch
        
        print(f"🎨 Loading local image model: {IMAGE_GENERATION_MODEL}")
        
        # Check if CUDA is available
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")
        
        # Load the SDXL pipeline
        pipe = StableDiffusionXLPipeline.from_pretrained(
            IMAGE_GENERATION_MODEL,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            use_safetensors=True,
            variant="fp16" if device == "cuda" else None
        )
        
        if device == "cuda":
            pipe = pipe.to("cuda")
            # Enable memory efficient attention
            pipe.enable_attention_slicing()
            pipe.enable_model_cpu_offload()
        
        # Generate image
        image = pipe(
            prompt=prompt,
            width=IMAGE_SIZE[0],
            height=IMAGE_SIZE[1],
            num_inference_steps=30,  # Reduced for faster generation
            guidance_scale=7.5,
            num_images_per_prompt=1
        ).images[0]
        
        # Save the image
        image_path = os.path.join(TEMP_DIR, filename)
        image.save(image_path)
        
        log_info(f"Local image saved: {image_path}")
        return image_path
        
    except Exception as e:
        log_error(f"Local image generation failed for {filename}", e)
        raise ImageProcessingError(f"Local image generation failed: {e}")


def _generate_image_api(prompt: str, filename: str) -> str:
    """Generate image using Hugging Face API"""
    try:
        if not HUGGINGFACE_API_TOKEN:
            raise Exception("HUGGINGFACE_API_TOKEN not found in environment variables")
        
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "guidance_scale": 7.5,
                "num_inference_steps": 50,
                "width": IMAGE_SIZE[0],
                "height": IMAGE_SIZE[1]
            }
        }
        
        url = f"{HUGGINGFACE_API_URL}/{IMAGE_GENERATION_MODEL}"
        
        for attempt in range(MAX_RETRIES):
            try:
                log_info(f"Generating image (attempt {attempt + 1}): {filename}")
                response = requests.post(url, headers=headers, json=payload, timeout=API_TIMEOUT)
                
                if response.status_code == 503:
                    # Model is loading
                    estimated_time = 60  # Default wait time
                    try:
                        error_data = response.json()
                        estimated_time = error_data.get("estimated_time", 60)
                    except:
                        pass
                    print(f"Model is loading, waiting {estimated_time} seconds...")
                    time.sleep(estimated_time)
                    continue
                    
                elif response.status_code == 429:
                    print("Rate limit reached. Please wait and try again later.")
                    raise Exception("Rate limit reached")
                    
                elif response.status_code == 200:
                    # Save the image
                    image_path = os.path.join(TEMP_DIR, filename)
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                    
                    log_info(f"Image saved: {image_path}")
                    return image_path
                    
                else:
                    response.raise_for_status()
                    
            except requests.RequestException as e:
                if attempt == MAX_RETRIES - 1:
                    raise ImageProcessingError(f"Image generation failed after {MAX_RETRIES} attempts: {e}")
                time.sleep(RATE_LIMIT_WAIT)
        
        raise ImageProcessingError("Failed to generate image")
        
    except Exception as e:
        raise ImageProcessingError(f"Image generation failed: {e}")


def remove_white_background(image_path: str) -> Image.Image:
    """Remove white background from character image using color-based masking"""
    try:
        # Open the image
        img = Image.open(image_path).convert("RGBA")
        
        # Get image data
        data = img.getdata()
        
        # Create new data with transparent background
        new_data = []
        for item in data:
            # Check if pixel is close to white
            r, g, b, a = item
            if (r > BACKGROUND_REMOVE_THRESHOLD and 
                g > BACKGROUND_REMOVE_THRESHOLD and 
                b > BACKGROUND_REMOVE_THRESHOLD):
                # Make pixel transparent
                new_data.append((r, g, b, 0))
            else:
                # Keep pixel as is
                new_data.append(item)
        
        # Update image data
        img.putdata(new_data)
        
        log_info("White background removed successfully")
        return img
        
    except Exception as e:
        log_error(f"Error removing background from {image_path}", e)
        raise ImageProcessingError(f"Background removal failed: {e}")


def resize_character_for_background(character_img: Image.Image, background_img: Image.Image) -> Image.Image:
    """Resize character to fit appropriately on background"""
    try:
        bg_width, bg_height = background_img.size
        char_width, char_height = character_img.size
        
        # Calculate scale to make character fit nicely (about 60% of background height)
        target_height = int(bg_height * 0.6)
        scale_factor = target_height / char_height
        
        new_width = int(char_width * scale_factor)
        new_height = target_height
        
        # Resize character
        resized_character = character_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        log_info(f"Character resized from {char_width}x{char_height} to {new_width}x{new_height}")
        return resized_character
        
    except Exception as e:
        log_error("Error resizing character", e)
        raise ImageProcessingError(f"Character resizing failed: {e}")


def merge_character_and_background(character_path: str, background_path: str, output_filename: str) -> str:
    """Merge character and background images"""
    try:
        log_info("Starting image merge process...")
        
        # Open background image
        background = Image.open(background_path).convert("RGBA")
        
        # Remove white background from character and get RGBA image
        character = remove_white_background(character_path)
        
        # Resize character to fit background
        character_resized = resize_character_for_background(character, background)
        
        # Calculate position to center character horizontally and place at bottom
        bg_width, bg_height = background.size
        char_width, char_height = character_resized.size
        
        # Center horizontally, place near bottom (leaving some space)
        x_position = (bg_width - char_width) // 2
        y_position = bg_height - char_height - 20  # 20 pixels from bottom
        
        # Create a copy of background for merging
        merged = background.copy()
        
        # Paste character onto background using alpha channel as mask
        merged.paste(character_resized, (x_position, y_position), character_resized)
        
        # Convert back to RGB for final output
        final_image = Image.new("RGB", merged.size, (255, 255, 255))
        final_image.paste(merged, mask=merged.split()[-1])  # Use alpha channel as mask
        
        # Save the final merged image
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        final_image.save(output_path, "JPEG", quality=95)
        
        log_info(f"Successfully merged images. Output saved to: {output_path}")
        return output_path
        
    except Exception as e:
        log_error("Error merging images", e)
        raise ImageProcessingError(f"Image merging failed: {e}")


def create_story_visualization(character_prompt: str, background_prompt: str, story_title: str = "story") -> str:
    """Complete pipeline to create story visualization"""
    try:
        log_info("Starting story visualization creation...")
        
        # Generate timestamp for unique filenames
        timestamp = int(time.time())
        
        # Generate character image
        character_filename = f"character_{timestamp}.png"
        character_path = generate_image_from_prompt(character_prompt, character_filename)
        
        # Generate background image
        background_filename = f"background_{timestamp}.png"
        background_path = generate_image_from_prompt(background_prompt, background_filename)
        
        # Merge images
        output_filename = f"{story_title}_{timestamp}_final.jpg"
        final_image_path = merge_character_and_background(
            character_path, 
            background_path, 
            output_filename
        )
        
        # Clean up temporary files
        try:
            os.remove(character_path)
            os.remove(background_path)
            log_info("Temporary files cleaned up")
        except:
            pass  # Don't fail if cleanup doesn't work
        
        log_info(f"Story visualization completed: {final_image_path}")
        return final_image_path
        
    except Exception as e:
        log_error("Error creating story visualization", e)
        raise ImageProcessingError(f"Story visualization failed: {e}")


def test_image_generation():
    """Test function for image generation pipeline"""
    try:
        test_character_prompt = "A brave knight in shining armor, full body shot, isolated on pure white background, png style, no background"
        test_background_prompt = "A mystical forest at dawn, sunlight filtering through trees, magical atmosphere"
        
        result = create_story_visualization(test_character_prompt, test_background_prompt, "test")
        print(f"Test completed successfully! Output: {result}")
        return result
        
    except Exception as e:
        print(f"Test failed: {e}")
        return None
