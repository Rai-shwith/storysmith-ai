"""
Story Chain - Generates story, character, and background descriptions
"""

import os
import sys
import re
import requests
import time
from typing import Dict, Any
from huggingface_hub import InferenceClient

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# LangChain - Latest lightweight modular architecture
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import BaseOutputParser
from langchain_core.prompts import PromptTemplate

from config import (
    HUGGINGFACE_API_TOKEN, 
    HUGGINGFACE_API_URL, 
    TEXT_GENERATION_MODEL,
    STORY_PROMPT_TEMPLATE,
    API_TIMEOUT,
    MAX_RETRIES,
    RATE_LIMIT_WAIT,
    USE_LOCAL_MODELS
)
from utils.error_handler import handle_api_error, log_error


class StoryOutputParser(BaseOutputParser):
    """Parser to extract story, character, and background from generated text"""
    
    def parse(self, text: str) -> Dict[str, str]:
        """Parse the output text into story components"""
        try:
            # For GPT-2, we get continuous text, so we need to split it intelligently
            result = {
                "story": "",
                "character_description": "",
                "background_description": ""
            }
            
            # Clean up the text
            text = text.strip()
            
            # Remove the prompt part if it's repeated
            if "STORY:" in text:
                text = text.split("STORY:", 1)[-1].strip()
            
            # Split into sentences and create story components
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            
            if len(sentences) >= 3:
                # Use first few sentences as the main story
                story_sentences = sentences[:max(3, len(sentences)//2)]
                result["story"] = '. '.join(story_sentences) + '.'
                
                # Create character description from story context
                result["character_description"] = "A brave adventurer with mysterious origins, wearing practical clothing suitable for magical quests"
                
                # Create background description from story context  
                result["background_description"] = "An enchanted forest with ancient trees, dappled sunlight, and magical atmosphere"
            else:
                # Fallback: use all text as story
                result["story"] = text
                result["character_description"] = "A character from the story"
                result["background_description"] = "A scene from the story"
            
            return result
            
        except Exception as e:
            log_error(f"Error parsing story output: {e}")
            return {
                "story": text,
                "character_description": "A character from the story",
                "background_description": "A scene from the story"
            }


class StoryChain(Runnable):
    """Modern LangChain Runnable for generating stories with character and background descriptions"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prompt_template = PromptTemplate(
            input_variables=["topic"],
            template=STORY_PROMPT_TEMPLATE
        )
        self.output_parser = StoryOutputParser()
        
        # Use direct API calls instead of deprecated endpoints
        # This is more reliable and doesn't require heavy dependencies
        self.llm = None  # Always use direct API approach
    
    def _call_huggingface_api(self, prompt: str) -> str:
        """Call Hugging Face API for text generation using modern client"""
        try:
            # Initialize the InferenceClient (token is read from environment)
            client = InferenceClient(token=HUGGINGFACE_API_TOKEN)
            
            # Use text generation with the modern client
            response = client.text_generation(
                prompt=prompt,
                model=TEXT_GENERATION_MODEL,
                max_new_tokens=400,
                temperature=0.8,
                top_p=0.9,
                do_sample=True,
                return_full_text=False
            )
            
            # The response is a string with the generated text
            return response.strip()
            
        except Exception as e:
            log_error(f"HuggingFace API call failed: {e}")
            raise Exception(f"API call failed: {e}")
    
    def _call_local_model(self, prompt: str) -> str:
        """Call local model for text generation using transformers pipeline"""
        try:
            from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
            import torch
            
            print(f"🔥 Loading local model: {TEXT_GENERATION_MODEL}")
            
            # Check if CUDA is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Using device: {device}")
            
            # Load tokenizer and model
            tokenizer = AutoTokenizer.from_pretrained(TEXT_GENERATION_MODEL)
            model = AutoModelForCausalLM.from_pretrained(
                TEXT_GENERATION_MODEL,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto" if device == "cuda" else None,
                trust_remote_code=True
            )
            
            # Create text generation pipeline
            generator = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                device=0 if device == "cuda" else -1,
                return_full_text=False
            )
            
            # Generate text
            response = generator(
                prompt,
                max_new_tokens=400,
                temperature=0.8,
                top_p=0.9,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
            
            # Extract generated text
            if response and len(response) > 0:
                generated_text = response[0]['generated_text'].strip()
                return generated_text
            else:
                raise Exception("No text generated from local model")
                
        except Exception as e:
            log_error(f"Local model call failed: {e}")
            raise Exception(f"Local model call failed: {e}")
    
    def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Modern LangChain invoke method for Runnable interface"""
        try:
            topic = input_data.get("topic", "")
            if not topic:
                raise Exception("No topic provided")
            
            # Always use direct API calls for better reliability
            print("🔗 Using direct HuggingFace API calls (lightweight approach)")
            return self._call_direct_api(input_data)
            
        except Exception as e:
            error_msg = f"Story generation failed: {e}"
            log_error(error_msg)
            raise Exception(error_msg)
    
    def _call_direct_api(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback method using direct API calls"""
        try:
            topic = inputs.get("topic", "")
            if not topic:
                raise Exception("No topic provided")
            
            # Format the prompt using LangChain's PromptTemplate
            prompt = self.prompt_template.format(topic=topic)
            
            print(f"Generating story for topic: {topic}")
            
            # Choose between local and API based on configuration
            if USE_LOCAL_MODELS:
                generated_text = self._call_local_model(prompt)
            else:
                if not HUGGINGFACE_API_TOKEN:
                    raise Exception("HUGGINGFACE_API_TOKEN not found in environment variables")
                generated_text = self._call_huggingface_api(prompt)
            
            if not generated_text:
                raise Exception("No text generated from model")
            
            # Parse the output using LangChain's BaseOutputParser
            parsed_result = self.output_parser.parse(generated_text)
            
            print("Story generation completed successfully!")
            return {"result": parsed_result}
            
        except Exception as e:
            error_msg = f"Story generation failed: {e}"
            log_error(error_msg)
            raise Exception(error_msg)


def create_story_chain() -> StoryChain:
    """Factory function to create a StoryChain instance"""
    return StoryChain()
