"""
Enhanced Story Chain with Integrated Image Generation
Combines story generation, prompt optimization, and image generation in a single LangChain pipeline
"""

import os
import sys
import time
from typing import Dict, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# LangChain imports
from langchain_core.runnables import Runnable

# Import existing components
from chains.story_chain import create_story_chain
from chains.image_prompt_chain import create_image_prompt_chain
from utils.image_merge import generate_image_from_prompt, merge_character_and_background
from utils.error_handler import log_info, log_error, StorySmithError
from config import OUTPUT_DIR


class EnhancedStoryVisualizationChain(Runnable):
    """
    Complete LangChain pipeline that:
    1. Generates story content (story, character desc, background desc)
    2. Optimizes descriptions into image prompts
    3. Generates character and background images
    4. Merges images into final visualization
    5. Returns complete story package with images
    """
    
    def __init__(self, generate_images: bool = True):
        super().__init__()
        self.generate_images = generate_images
        self.story_chain = create_story_chain()
        self.prompt_chain = create_image_prompt_chain()
    
    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete story visualization pipeline"""
        try:
            topic = input_data.get("topic", "")
            log_info(f"Starting enhanced story visualization for: {topic}")
            
            print("🎯 Starting Enhanced Story Generation Pipeline...")
            print("=" * 60)
            
            # Step 1: Generate Story Content
            print("📝 Step 1: Generating story content...")
            story_result = self.story_chain.invoke({"topic": topic})
            story_data = story_result["result"]
            
            print("✅ Story content generated!")
            print(f"   📖 Story: {len(story_data['story'])} characters")
            print(f"   👤 Character: {story_data['character_description'][:50]}...")
            print(f"   🏞️  Background: {story_data['background_description'][:50]}...")
            
            result = {
                "topic": topic,
                "timestamp": datetime.now().isoformat(),
                "story": story_data["story"],
                "character_description": story_data["character_description"],
                "background_description": story_data["background_description"],
                "character_image_path": None,
                "background_image_path": None,
                "final_image_path": None,
                "character_prompt": None,
                "background_prompt": None,
                "detected_style": None
            }
            
            if not self.generate_images:
                print("⏭️  Image generation skipped (generate_images=False)")
                return result
            
            # Step 2: Optimize Image Prompts
            print("\n🎨 Step 2: Optimizing image prompts...")
            prompt_result = self.prompt_chain.invoke({"story_data": story_data})
            image_prompts = prompt_result["image_prompts"]
            
            result["character_prompt"] = image_prompts["character_prompt"]
            result["background_prompt"] = image_prompts["background_prompt"]
            result["detected_style"] = image_prompts["detected_style"]
            
            print(f"✅ Image prompts optimized!")
            print(f"   🎭 Style detected: {image_prompts['detected_style']}")
            print(f"   👤 Character prompt: {image_prompts['character_prompt'][:60]}...")
            print(f"   🏞️  Background prompt: {image_prompts['background_prompt'][:60]}...")
            
            # Step 3: Generate Images
            print("\n🖼️  Step 3: Generating images...")
            timestamp = int(time.time())
            
            # Generate character image
            print("   📷 Generating character image...")
            character_filename = f"character_{timestamp}.png"
            character_path = generate_image_from_prompt(
                image_prompts["character_prompt"], 
                character_filename
            )
            result["character_image_path"] = character_path
            print(f"   ✅ Character image: {character_path}")
            
            # Generate background image
            print("   📷 Generating background image...")
            background_filename = f"background_{timestamp}.png"
            background_path = generate_image_from_prompt(
                image_prompts["background_prompt"], 
                background_filename
            )
            result["background_image_path"] = background_path
            print(f"   ✅ Background image: {background_path}")
            
            # Step 4: Merge Images
            print("\n🔗 Step 4: Merging images...")
            story_title = topic.replace(" ", "_").lower()[:20]  # Truncate for filename
            output_filename = f"{story_title}_{timestamp}_final.jpg"
            
            final_image_path = merge_character_and_background(
                character_path,
                background_path,
                output_filename
            )
            result["final_image_path"] = final_image_path
            print(f"   ✅ Final image: {final_image_path}")
            
            # Step 5: Save Summary
            self._save_story_summary(result)
            
            print("\n🎉 COMPLETE STORY VISUALIZATION PIPELINE FINISHED! 🎉")
            print("=" * 60)
            print(f"📁 Final image: {final_image_path}")
            print(f"📝 Story summary saved")
            print("=" * 60)
            
            return result
            
        except Exception as e:
            error_msg = f"Enhanced story visualization failed: {e}"
            log_error(error_msg)
            raise StorySmithError(error_msg)
    
    def _save_story_summary(self, result: Dict[str, Any]):
        """Save a comprehensive summary of the generated story and images"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_file = os.path.join(OUTPUT_DIR, f"enhanced_story_summary_{timestamp}.txt")
            
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write("StorySmith AI - Enhanced Story Generation Summary\n")
                f.write("=" * 60 + "\n")
                f.write(f"Generated on: {result['timestamp']}\n")
                f.write(f"Topic: {result['topic']}\n")
                f.write(f"Detected Style: {result.get('detected_style', 'N/A')}\n\n")
                
                f.write("STORY:\n")
                f.write("-" * 30 + "\n")
                f.write(f"{result['story']}\n\n")
                
                f.write("CHARACTER DESCRIPTION:\n")
                f.write("-" * 30 + "\n")
                f.write(f"{result['character_description']}\n\n")
                
                f.write("BACKGROUND DESCRIPTION:\n")
                f.write("-" * 30 + "\n")
                f.write(f"{result['background_description']}\n\n")
                
                if result.get('character_prompt'):
                    f.write("IMAGE PROMPTS:\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"Character: {result['character_prompt']}\n\n")
                    f.write(f"Background: {result['background_prompt']}\n\n")
                
                if result.get('final_image_path'):
                    f.write("GENERATED FILES:\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"Character Image: {result.get('character_image_path', 'N/A')}\n")
                    f.write(f"Background Image: {result.get('background_image_path', 'N/A')}\n")
                    f.write(f"Final Merged Image: {result['final_image_path']}\n")
            
            log_info(f"Story summary saved: {summary_file}")
            
        except Exception as e:
            log_error("Failed to save story summary", e)

def create_enhanced_story_chain(generate_images: bool = True) -> EnhancedStoryVisualizationChain:
    """Factory function to create the enhanced story visualization chain"""
    return EnhancedStoryVisualizationChain(generate_images=generate_images)


def create_simple_story_chain() -> EnhancedStoryVisualizationChain:
    """Create a chain that only generates story content, no images"""
    return EnhancedStoryVisualizationChain(generate_images=False)
