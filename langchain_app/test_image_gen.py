#!/usr/bin/env python3
"""
Test SDXL image generation capability
"""

import os
import sys
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import torch
    from diffusers import StableDiffusionXLPipeline
except ImportError as e:
    import logging
    logger = logging.getLogger(__name__)
    log_error(f"Import error: {e}")
    log_error("Install required packages: pip install torch diffusers")
    sys.exit(1)

from config import USE_LOCAL_MODELS, IMAGE_GENERATION_MODEL, IMAGE_SIZE, OUTPUT_DIR
from utils.error_handler import log_info, log_error, log_warning

# Get logger for this module
logger = logging.getLogger(__name__)

def main():
    logger.info("🎨 Testing SDXL Image Generation")
    logger.info("=" * 40)
    
    # Check system
    logger.info(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        logger.info(f"GPU: {torch.cuda.get_device_name()}")
        logger.info(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB")
    
    # Check config
    logger.info(f"USE_LOCAL_MODELS: {USE_LOCAL_MODELS}")
    logger.info(f"IMAGE_MODEL: {IMAGE_GENERATION_MODEL}")
    logger.info(f"IMAGE_SIZE: {IMAGE_SIZE}")
    
    if not USE_LOCAL_MODELS:
        log_error("❌ Local models disabled. Set USE_LOCAL_MODELS=True in config")
        return
    
    try:
        logger.info("\n🔥 Loading SDXL pipeline...")
        from diffusers import StableDiffusionXLPipeline
        import os
        
        # Set environment variables for better download performance
        os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"  # Use faster download client
        
        # Authentication is handled by the cached token from huggingface-cli login
        logger.info("🔑 Using cached HuggingFace authentication...")
        
        # Load pipeline - using correct SDXL model name with better download settings
        model_name = "stabilityai/stable-diffusion-xl-base-1.0"  # Correct model name
        logger.info(f"Loading model: {model_name}")
        
        # Try with better download settings
        pipe = StableDiffusionXLPipeline.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
            resume_download=True,  # Resume interrupted downloads
            local_files_only=False,  # Allow fresh downloads
            force_download=False  # Don't re-download if already cached
        )
        
        if torch.cuda.is_available():
            pipe = pipe.to("cuda")
            pipe.enable_attention_slicing()
            pipe.enable_model_cpu_offload()
        
        logger.info("✅ SDXL pipeline loaded successfully!")
        
        # Test generation
        test_prompt = "A friendly robot in a garden, digital art"
        logger.info(f"\n🎨 Generating test image with prompt: {test_prompt}")
        
        image = pipe(
            prompt=test_prompt,
            width=512,
            height=512,
            num_inference_steps=20,  # Fast test
            guidance_scale=7.5
        ).images[0]
        
        # Save image
        output_path = os.path.join(OUTPUT_DIR, "test_robot.png")
        image.save(output_path)
        
        logger.info(f"✅ Test image generated: {output_path}")
        return True
        
    except Exception as e:
        log_error(f"❌ Image generation failed: {e}")
        return False

def test_image_generation():
    """Function to test image generation"""
    return main()

if __name__ == "__main__":
    test_image_generation()
