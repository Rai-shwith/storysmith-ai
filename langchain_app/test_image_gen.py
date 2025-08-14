#!/usr/bin/env python3
"""
Simple test script for SDXL image generation
"""

import torch
import os
from config import USE_LOCAL_MODELS, IMAGE_GENERATION_MODEL, IMAGE_SIZE, OUTPUT_DIR

def test_image_generation():
    """Test local SDXL image generation"""
    print("🎨 Testing SDXL Image Generation")
    print("=" * 40)
    
    # Check CUDA
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU: {torch.cuda.get_device_name()}")
        print(f"GPU memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f}GB")
    
    # Check config
    print(f"USE_LOCAL_MODELS: {USE_LOCAL_MODELS}")
    print(f"IMAGE_MODEL: {IMAGE_GENERATION_MODEL}")
    print(f"IMAGE_SIZE: {IMAGE_SIZE}")
    
    if not USE_LOCAL_MODELS:
        print("❌ Local models disabled. Set USE_LOCAL_MODELS=True in config")
        return False
    
    try:
        print("\n🔥 Loading SDXL pipeline...")
        from diffusers import StableDiffusionXLPipeline
        import os
        
        # Set environment variables for better download performance
        os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "1"  # Use faster download client
        
        # Authentication is handled by the cached token from huggingface-cli login
        print("🔑 Using cached HuggingFace authentication...")
        
        # Load pipeline - using correct SDXL model name with better download settings
        model_name = "stabilityai/stable-diffusion-xl-base-1.0"  # Correct model name
        print(f"Loading model: {model_name}")
        
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
        
        print("✅ SDXL pipeline loaded successfully!")
        
        # Test generation
        test_prompt = "A friendly robot in a garden, digital art"
        print(f"\n🎨 Generating test image with prompt: {test_prompt}")
        
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
        
        print(f"✅ Test image generated: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Image generation failed: {e}")
        return False

if __name__ == "__main__":
    test_image_generation()
