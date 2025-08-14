"""
Image Prompt Chain - Converts story descriptions to optimized image generation prompts
"""

import os
import sys
import re
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# LangChain - Latest modular architecture
from langchain_core.runnables import Runnable

from config import (
    CHARACTER_IMAGE_PROMPT_TEMPLATE,
    BACKGROUND_IMAGE_PROMPT_TEMPLATE,
    STYLE_MODIFIERS
)
from utils.error_handler import log_error


class ImagePromptChain(Runnable):
    """Modern LangChain Runnable for converting character and background descriptions to image prompts"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def _detect_style(self, story_text: str) -> str:
        """Detect the style/genre of the story to apply appropriate modifiers"""
        story_lower = story_text.lower()
        
        # Keywords for different genres
        genre_keywords = {
            "fantasy": ["magic", "wizard", "dragon", "spell", "enchanted", "mystical", "fairy", "quest"],
            "sci-fi": ["space", "robot", "alien", "future", "technology", "cyber", "laser", "spaceship"],
            "horror": ["dark", "scary", "ghost", "monster", "haunted", "evil", "shadow", "nightmare"],
            "romance": ["love", "heart", "romantic", "kiss", "wedding", "passion", "beautiful", "tender"],
            "adventure": ["journey", "explore", "treasure", "mountain", "forest", "adventure", "brave", "hero"],
            "mystery": ["mystery", "detective", "clue", "secret", "hidden", "investigate", "solve", "puzzle"]
        }
        
        # Count matches for each genre
        genre_scores = {}
        for genre, keywords in genre_keywords.items():
            score = sum(1 for keyword in keywords if keyword in story_lower)
            if score > 0:
                genre_scores[genre] = score
        
        # Return the genre with highest score, or default
        if genre_scores:
            return max(genre_scores, key=genre_scores.get)
        return "default"
    
    def _clean_description(self, description: str) -> str:
        """Clean and optimize description for image generation"""
        # Remove common filler words and phrases that don't help image generation
        filler_phrases = [
            "in the story", "from the tale", "as described", "mentioned in",
            "the character", "the person", "the individual"
        ]
        
        cleaned = description
        for phrase in filler_phrases:
            cleaned = re.sub(phrase, "", cleaned, flags=re.IGNORECASE)
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        # Ensure it ends properly
        if cleaned and not cleaned.endswith('.'):
            cleaned += '.'
        
        return cleaned
    
    def _enhance_character_prompt(self, character_desc: str, style: str) -> str:
        """Create optimized character prompt for image generation"""
        cleaned_desc = self._clean_description(character_desc)
        style_modifier = STYLE_MODIFIERS.get(style, STYLE_MODIFIERS["default"])
        
        # Add specific instructions for better character generation
        enhanced_prompt = CHARACTER_IMAGE_PROMPT_TEMPLATE.format(
            character_description=cleaned_desc,
            style_modifier=style_modifier
        )
        
        return enhanced_prompt
    
    def _enhance_background_prompt(self, background_desc: str, style: str) -> str:
        """Create optimized background prompt for image generation"""
        cleaned_desc = self._clean_description(background_desc)
        style_modifier = STYLE_MODIFIERS.get(style, STYLE_MODIFIERS["default"])
        
        # Add specific instructions for better background generation
        enhanced_prompt = BACKGROUND_IMAGE_PROMPT_TEMPLATE.format(
            background_description=cleaned_desc,
            style_modifier=style_modifier
        )
        
        return enhanced_prompt
    
    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Modern LangChain invoke method for Runnable interface"""
        try:
            story_data = input_data.get("story_data", {})
            
            # Debug: Print the story_data structure
            print(f"Debug - story_data keys: {list(story_data.keys())}")
            print(f"Debug - story_data type: {type(story_data)}")
            
            # Extract components with better error handling
            story = story_data.get("story", "")
            character_desc = story_data.get("character_description", "")
            background_desc = story_data.get("background_description", "")
            
            if not story:
                print("Warning: No story found in story_data")
            if not character_desc:
                print("Warning: No character_description found in story_data")
            if not background_desc:
                print("Warning: No background_description found in story_data")
            
            print("Generating optimized image prompts...")
            
            # Detect style from story
            detected_style = self._detect_style(story)
            print(f"Detected style: {detected_style}")
            
            # Generate enhanced prompts
            character_prompt = self._enhance_character_prompt(character_desc, detected_style)
            background_prompt = self._enhance_background_prompt(background_desc, detected_style)
            
            result = {
                "character_prompt": character_prompt,
                "background_prompt": background_prompt,
                "detected_style": detected_style,
                "original_character_desc": character_desc,
                "original_background_desc": background_desc
            }
            
            print("Image prompts generated successfully!")
            print(f"Character prompt: {character_prompt[:100]}...")
            print(f"Background prompt: {background_prompt[:100]}...")
            
            return {"image_prompts": result}
            
        except Exception as e:
            error_msg = f"Image prompt generation failed: {e}"
            log_error(error_msg)
            # Print more debug info
            print(f"Debug - Exception details: {e}")
            print(f"Debug - input_data: {input_data}")
            raise Exception(error_msg)


def create_image_prompt_chain() -> ImagePromptChain:
    """Factory function to create an ImagePromptChain instance"""
    return ImagePromptChain()
