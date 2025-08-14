"""
Story Chain - Functional approach for generating story, character, and background descriptions
Uses LangChain's latest patterns with pipe operations and functional composition
"""

import os
import sys
import re
import torch
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# LangChain imports
from langchain_huggingface import HuggingFacePipeline
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from huggingface_hub import InferenceClient
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Config and utilities
from config import (
    HUGGINGFACE_API_TOKEN,
    TEXT_GENERATION_MODEL,
    STORY_PROMPT_TEMPLATE,
    CHARACTER_PROMPT_TEMPLATE,
    BACKGROUND_PROMPT_TEMPLATE,
    USE_LOCAL_MODELS,
    API_TIMEOUT,
    MAX_RETRIES
)
from utils.error_handler import log_error


def clean_repetitive_text(text: str) -> str:
    """Remove repetitive sentences and clean up the text."""
    sentences = text.split('. ')
    cleaned_sentences = []
    seen_sentences = set()

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and sentence.lower() not in seen_sentences:
            seen_sentences.add(sentence.lower())
            cleaned_sentences.append(sentence)

    result = '. '.join(cleaned_sentences)
    if result and not result.endswith('.'):
        result += '.'

    return result


def enforce_png_format(text: str) -> str:
    """Ensure text ends with PNG format specification."""
    text = text.strip()
    if not text.lower().endswith("transparent background, png format."):
        text = re.sub(r'\.*$', '', text)  # remove trailing dots
        text += ". transparent background, PNG format"
    return text


def extract_clean_response(text: str) -> str:
    """Extract only the model's response, removing all instruction artifacts."""
    # First, try to find the assistant's response section
    if "<|assistant|>" in text:
        # Split and get everything after the assistant marker
        parts = text.split("<|assistant|>")
        if len(parts) > 1:
            response = parts[-1]
            # Remove end markers
            response = response.replace("<|end|>", "").strip()
            return response

    # Fallback: use the original cleaning
    return clean_model_output(text)


def clean_model_output(text: str) -> str:
    """Clean the output from instruction-following models."""
    # Remove instruction tags and clean up
    text = text.replace("<|user|>", "").replace("<|assistant|>", "").replace("<|end|>", "")
    text = text.replace("<s>", "").replace("</s>", "")
    text = text.replace("[INST]", "").replace("[/INST]", "")

    # Find the actual response (usually after the instruction)
    lines = text.split('\n')
    clean_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith(('<', '[', 'Based on', 'Write a', 'Describe', 'Provide', 'Create a', 'Story:', 'Focus on')):
            clean_lines.append(line)

    if clean_lines:
        result = ' '.join(clean_lines)
        # Remove any instruction artifacts that might remain
        result = re.sub(r'(Create a detailed|Write 4-5|Include:|Based on this).*?(?=\w)', '', result)
        return result.strip()
    return text.strip()


def load_local_llm():
    """Load local LLM using HuggingFacePipeline."""
    try:
        print(f"🔥 Loading local model: {TEXT_GENERATION_MODEL}")
        
        # Check if CUDA is available and set device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device}")

        tokenizer = AutoTokenizer.from_pretrained(
            TEXT_GENERATION_MODEL,
            trust_remote_code=True
        )
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token

        model = AutoModelForCausalLM.from_pretrained(
            TEXT_GENERATION_MODEL,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto",
            trust_remote_code=True,
            attn_implementation="eager"  # Use eager attention to avoid cache issues
        )

        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=400,  # Increased to prevent truncation
            min_new_tokens=60,
            repetition_penalty=1.1,
            do_sample=True,
            temperature=0.4,
            top_p=0.9,
            top_k=50,
            pad_token_id=tokenizer.eos_token_id,
            use_cache=False  # Disable caching to avoid the seen_tokens issue
        )

        return HuggingFacePipeline(pipeline=pipe)
    
    except Exception as e:
        log_error(f"Failed to load local model: {e}")
        raise Exception(f"Local model loading failed: {e}")


def create_api_llm():
    """Create LLM wrapper for HuggingFace Inference API."""
    
    class HuggingFaceAPILLM:
        """Simple LLM wrapper for HuggingFace Inference API."""
        
        def __init__(self):
            if not HUGGINGFACE_API_TOKEN:
                raise Exception("HUGGINGFACE_API_TOKEN not found in environment variables")
            self.client = InferenceClient(token=HUGGINGFACE_API_TOKEN)
        
        def invoke(self, prompt: str) -> str:
            """Call HuggingFace Inference API."""
            try:
                response = self.client.text_generation(
                    prompt=prompt,
                    model=TEXT_GENERATION_MODEL,
                    max_new_tokens=400,
                    temperature=0.4,
                    top_p=0.9,
                    do_sample=True,
                    return_full_text=False
                )
                return response.strip()
            except Exception as e:
                log_error(f"HuggingFace API call failed: {e}")
                raise Exception(f"API call failed: {e}")
    
    return HuggingFaceAPILLM()


def get_llm():
    """Get LLM based on USE_LOCAL_MODELS configuration."""
    if USE_LOCAL_MODELS:
        return load_local_llm()
    else:
        return create_api_llm()


def generate_story_bundle(user_prompt: str) -> Dict[str, str]:
    """
    Generate story, character, and background descriptions.
    
    Args:
        user_prompt: The topic or prompt for story generation
        
    Returns:
        Dictionary with 'story', 'character_description', and 'background_description' keys
    """
    try:
        print(f"🔗 Generating story bundle for: {user_prompt}")
        print(f"📍 Using {'local models' if USE_LOCAL_MODELS else 'API calls'}")
        
        # Get LLM instance
        llm = get_llm()
        
        # Create prompt templates
        story_prompt = PromptTemplate.from_template(STORY_PROMPT_TEMPLATE)
        character_prompt = PromptTemplate.from_template(CHARACTER_PROMPT_TEMPLATE)
        background_prompt = PromptTemplate.from_template(BACKGROUND_PROMPT_TEMPLATE)
        
        # Build pipeline chains
        story_chain = story_prompt | llm | StrOutputParser()
        character_chain = character_prompt | llm | StrOutputParser()
        background_chain = background_prompt | llm | StrOutputParser()
        
        print("📝 Generating story...")
        # First, generate the story
        story_text = story_chain.invoke({"topic": user_prompt})
        
        print("👤 Generating character description...")
        # Then generate character and background descriptions based on the story
        character_text = character_chain.invoke({"story": story_text})
        
        print("🌄 Generating background description...")
        background_text = background_chain.invoke({"story": story_text})
        
        # Clean and format outputs
        result = {
            "story": clean_repetitive_text(extract_clean_response(story_text.strip())),
            "character_description": enforce_png_format(clean_repetitive_text(extract_clean_response(character_text.strip()))),
            "background_description": clean_repetitive_text(extract_clean_response(background_text.strip()))
        }
        
        print("✅ Story bundle generation completed successfully!")
        return result
        
    except Exception as e:
        error_msg = f"Story bundle generation failed: {e}"
        log_error(error_msg)
        raise Exception(error_msg)


def create_story_chain():
    """
    Factory function for compatibility with existing code.
    """
    def invoke(input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke the story generation with the expected input/output format."""
        try:
            topic = input_data.get("topic", "")
            if not topic:
                raise Exception("No topic provided")
            
            # Generate story bundle
            result = generate_story_bundle(topic)
            
            # Return in the expected format for compatibility
            return {"result": result}
            
        except Exception as e:
            error_msg = f"Story generation failed: {e}"
            log_error(error_msg)
            raise Exception(error_msg)
    
    # Return an object that has an invoke method
    class StoryChainCompat:
        def invoke(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
            return invoke(input_data)
    
    return StoryChainCompat()


# Main function for direct usage
if __name__ == "__main__":
    # Example usage
    result = generate_story_bundle("a friendly robot")
    print("\n📖 Generated Story Bundle:")
    print(f"Story: {result['story']}")
    print(f"Character: {result['character_description']}")
    print(f"Background: {result['background_description']}")
