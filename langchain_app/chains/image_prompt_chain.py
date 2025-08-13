from diffusers import StableDiffusionPipeline
from PIL import Image, ImageFilter
import torch
import numpy as np
import os
import re

class ImageGenerator:
    def __init__(self):
        self.pipe = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def load_diffusion_pipeline(self):
        """Load Stable Diffusion pipeline for image generation."""
        if self.pipe is None:
            print("Loading Stable Diffusion pipeline...")
            # Using a lighter, faster model suitable for Colab
            model_id = "runwayml/stable-diffusion-v1-5"
            
            self.pipe = StableDiffusionPipeline.from_pretrained(
                model_id,
                torch_dtype=torch.float16,
                safety_checker=None,
                requires_safety_checker=False
            )
            
            if torch.cuda.is_available():
                self.pipe = self.pipe.to("cuda")
            
            # Enable memory efficient attention for Colab
            self.pipe.enable_attention_slicing()
            try:
                self.pipe.enable_xformers_memory_efficient_attention()
            except:
                print("xformers not available, using standard attention")
            
            print("Pipeline loaded successfully!")
        return self.pipe

    def create_transparent_background(self, image: Image.Image) -> Image.Image:
        """Convert white/light backgrounds to transparent."""
        # Convert to RGBA if not already
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Get image data
        data = np.array(image)
        
        # Define white/light background threshold
        threshold = 240
        
        # Create mask for pixels that are close to white
        mask = (data[:, :, 0] > threshold) & (data[:, :, 1] > threshold) & (data[:, :, 2] > threshold)
        
        # Set alpha channel to 0 for white pixels
        data[mask, 3] = 0
        
        # Create new image with transparency
        transparent_image = Image.fromarray(data, 'RGBA')
        
        return transparent_image

    def enhance_character_prompt(self, character_prompt: str) -> str:
        """Add professional quality tags to character prompt."""
        # Remove any existing PNG format text for processing
        clean_prompt = re.sub(r'\.?\s*transparent background,?\s*png format\.?', '', character_prompt, flags=re.IGNORECASE)
        
        # Add quality and style tags
        quality_tags = "high quality, detailed, masterpiece, best quality, sharp focus, professional digital art"
        negative_concepts = "isolated character"
        
        enhanced = f"{clean_prompt}, {quality_tags}, {negative_concepts}, transparent background, PNG format"
        return enhanced

    def enhance_background_prompt(self, background_prompt: str) -> str:
        """Add professional quality tags to background prompt."""
        quality_tags = "high quality, detailed, masterpiece, best quality, sharp focus, cinematic lighting, professional environment art"
        composition_tags = "wide shot, establishing shot, detailed environment"
        
        enhanced = f"{background_prompt}, {quality_tags}, {composition_tags}"
        return enhanced

    def generate_character_image(self, character_prompt: str, output_path: str = None) -> Image.Image:
        """Generate character image with transparent background."""
        pipe = self.load_diffusion_pipeline()
        
        # Enhance the prompt
        enhanced_prompt = self.enhance_character_prompt(character_prompt)
        print(f"Generating character with prompt: {enhanced_prompt[:100]}...")
        
        # Add negative prompts for better quality
        negative_prompt = "background, environment, landscape, multiple people, crowd, blurry, low quality, distorted, text, watermark, signature, frame, border"
        
        # Generate image
        image = pipe(
            prompt=enhanced_prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=25,  # Reduced for faster generation in Colab
            guidance_scale=7.5,
            width=512,
            height=512,
            generator=torch.Generator(device=self.device).manual_seed(42)  # For reproducible results
        ).images[0]
        
        # Create transparent background
        transparent_image = self.create_transparent_background(image)
        
        # Save if path provided
        if output_path:
            transparent_image.save(output_path, "PNG")
            print(f"Character image saved to: {output_path}")
        
        return transparent_image

    def generate_background_image(self, background_prompt: str, output_path: str = None) -> Image.Image:
        """Generate background image."""
        pipe = self.load_diffusion_pipeline()
        
        # Enhance the prompt
        enhanced_prompt = self.enhance_background_prompt(background_prompt)
        print(f"Generating background with prompt: {enhanced_prompt[:100]}...")
        
        # Add negative prompts
        negative_prompt = "people, characters, animals, faces, humans, crowd, low quality, blurry, distorted, text, watermark, signature"
        
        # Generate wider background image
        image = pipe(
            prompt=enhanced_prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=25,  # Reduced for faster generation
            guidance_scale=7.5,
            width=768,
            height=512,
            generator=torch.Generator(device=self.device).manual_seed(123)  # Different seed for variety
        ).images[0]
        
        # Save if path provided
        if output_path:
            image.save(output_path, "PNG")
            print(f"Background image saved to: {output_path}")
        
        return image

    def merge_character_and_background(self, character_img: Image.Image, background_img: Image.Image, 
                                     character_position: tuple = None, character_scale: float = 1.0) -> Image.Image:
        """Merge character image onto background."""
        # Resize background to standard size if needed
        background = background_img.resize((768, 512), Image.Resampling.LANCZOS)
        
        # Calculate character position (default: center-bottom)
        if character_position is None:
            char_width, char_height = character_img.size
            bg_width, bg_height = background.size
            
            # Scale character to fit nicely in the scene
            max_char_height = int(bg_height * 0.7)  # Character takes up 70% of background height
            if char_height > max_char_height:
                scale_factor = max_char_height / char_height
                character_scale *= scale_factor
        
        # Scale character if needed
        if character_scale != 1.0:
            new_size = (
                int(character_img.size[0] * character_scale),
                int(character_img.size[1] * character_scale)
            )
            character_img = character_img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Calculate final position
        if character_position is None:
            char_width, char_height = character_img.size
            bg_width, bg_height = background.size
            x = (bg_width - char_width) // 2
            y = bg_height - char_height - 20  # 20px from bottom
            character_position = (x, y)
        
        # Create final image
        final_image = background.copy()
        final_image.paste(character_img, character_position, character_img)
        
        return final_image

def generate_story_images(story_bundle: dict, save_directory: str = "/content/drive/MyDrive/storysmith_images/") -> dict:
    """
    Generate all images from story bundle.
    
    Args:
        story_bundle: Dictionary with 'story', 'character', 'background' keys
        save_directory: Directory to save images
    
    Returns:
        Dictionary with generated images and file paths
    """
    # Create save directory
    os.makedirs(save_directory, exist_ok=True)
    
    # Initialize image generator
    generator = ImageGenerator()
    
    print("=== STARTING IMAGE GENERATION ===")
    print(f"Character prompt: {story_bundle['character']}")
    print(f"Background prompt: {story_bundle['background']}")
    
    # Generate images
    print("\n1. Generating character image...")
    char_path = os.path.join(save_directory, "character.png")
    character_image = generator.generate_character_image(story_bundle["character"], char_path)
    
    print("\n2. Generating background image...")
    bg_path = os.path.join(save_directory, "background.png")
    background_image = generator.generate_background_image(story_bundle["background"], bg_path)
    
    print("\n3. Merging images...")
    merged_path = os.path.join(save_directory, "final_scene.png")
    merged_image = generator.merge_character_and_background(character_image, background_image)
    merged_image.save(merged_path)
    print(f"Final scene saved to: {merged_path}")
    
    print("\n=== IMAGE GENERATION COMPLETE ===")
    
    return {
        "character_image": character_image,
        "background_image": background_image,
        "merged_image": merged_image,
        "character_path": char_path,
        "background_path": bg_path,
        "merged_path": merged_path
    }

def test_image_generation():
    """Test function for image generation."""
    # Test story bundle
    test_bundle = {
        "story": "A brave knight in shining armor stands before a dark castle.",
        "character": "A tall knight wearing gleaming silver armor, holding a sword, confident pose. transparent background, PNG format",
        "background": "A dark gothic castle on a hill, stormy sky, dramatic lighting, medieval fantasy setting"
    }
    
    print("Testing image generation...")
    result = generate_story_images(test_bundle, "/content/drive/MyDrive/test_images/")
    return result

if __name__ == "__main__":
    test_image_generation()
