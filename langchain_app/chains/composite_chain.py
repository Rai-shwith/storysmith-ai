"""
Modern LangChain Composite Chain for complete story and visualization pipeline
Demonstrates LangChain's latest Runnable interface and chain composition
"""

import os
import sys
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.runnables.utils import Input, Output

from chains.story_chain import create_story_chain
from chains.image_prompt_chain import create_image_prompt_chain
from utils.image_merge import create_story_visualization
from utils.error_handler import log_info, log_error
from config import OUTPUT_DIR


class StoryVisualizationChain(Runnable):
    """
    Modern LangChain composite chain that orchestrates the complete pipeline:
    Topic → Story Generation → Image Prompt Optimization → Image Generation & Merging
    """
    
    def __init__(self):
        super().__init__()
        self.story_chain = create_story_chain()
        self.prompt_chain = create_image_prompt_chain()
    
    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete story visualization pipeline using modern LangChain composition"""
        try:
            topic = input_data.get("topic", "")
            log_info(f"Starting complete story visualization for: {topic}")
            
            # Step 1: Story Generation Chain
            story_result = self.story_chain.invoke({"topic": topic})
            story_data = story_result["result"]
            
            # Step 2: Image Prompt Chain  
            prompt_result = self.prompt_chain.invoke({"story_data": story_data})
            image_prompts = prompt_result["image_prompts"]
            
            # Step 3: Image Generation (not part of LangChain, but integrated)
            story_title = topic.replace(" ", "_").lower()
            final_image_path = create_story_visualization(
                image_prompts["character_prompt"],
                image_prompts["background_prompt"],
                story_title
            )
            
            # Combine all results
            complete_result = {
                "topic": topic,
                "story": story_data["story"],
                "character_description": story_data["character_description"],
                "background_description": story_data["background_description"],
                "character_prompt": image_prompts["character_prompt"],
                "background_prompt": image_prompts["background_prompt"],
                "detected_style": image_prompts["detected_style"],
                "final_image_path": final_image_path
            }
            
            log_info("Complete story visualization pipeline completed successfully!")
            return complete_result
            
        except Exception as e:
            error_msg = f"Story visualization pipeline failed: {e}"
            log_error(error_msg)
            raise Exception(error_msg)
    
    def stream(self, input_data: Dict[str, Any]):
        """Stream intermediate results for real-time updates"""
        topic = input_data.get("topic", "")
        
        # Yield story generation progress
        yield {"step": "story_generation", "status": "starting", "topic": topic}
        
        try:
            story_result = self.story_chain.invoke({"topic": topic})
            story_data = story_result["result"]
            yield {"step": "story_generation", "status": "completed", "data": story_data}
            
            # Yield prompt optimization progress
            yield {"step": "prompt_optimization", "status": "starting"}
            prompt_result = self.prompt_chain.invoke({"story_data": story_data})
            image_prompts = prompt_result["image_prompts"]
            yield {"step": "prompt_optimization", "status": "completed", "data": image_prompts}
            
            # Yield image generation progress
            yield {"step": "image_generation", "status": "starting"}
            story_title = topic.replace(" ", "_").lower()
            final_image_path = create_story_visualization(
                image_prompts["character_prompt"],
                image_prompts["background_prompt"],
                story_title
            )
            yield {"step": "image_generation", "status": "completed", "image_path": final_image_path}
            
            # Final result
            complete_result = {
                "topic": topic,
                "story": story_data["story"],
                "character_description": story_data["character_description"],
                "background_description": story_data["background_description"],
                "character_prompt": image_prompts["character_prompt"],
                "background_prompt": image_prompts["background_prompt"],
                "detected_style": image_prompts["detected_style"],
                "final_image_path": final_image_path
            }
            
            yield {"step": "complete", "status": "success", "result": complete_result}
            
        except Exception as e:
            yield {"step": "error", "status": "failed", "error": str(e)}


def create_story_visualization_chain() -> StoryVisualizationChain:
    """Factory function to create the complete visualization chain"""
    return StoryVisualizationChain()


# Example of modern LangChain chain composition (for future use)
def create_advanced_chain():
    """
    Example of advanced LangChain chain composition using the new syntax
    This shows how we can compose chains in the modern LangChain way
    """
    story_chain = create_story_chain()
    prompt_chain = create_image_prompt_chain()
    
    # Modern LangChain chain composition with pipe operator
    # This would work if we had compatible input/output schemas
    # composite_chain = (
    #     {"topic": RunnablePassthrough()} 
    #     | story_chain 
    #     | {"story_data": lambda x: x["result"]}
    #     | prompt_chain
    # )
    
    return StoryVisualizationChain()  # For now, return our custom implementation
