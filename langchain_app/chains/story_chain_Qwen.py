from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough
import re
import torch

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

def extract_clean_response(text: str) -> str:
    """Extract only the model's response, removing all instruction artifacts."""
    # First, try to find the assistant's response section for Qwen format
    if "<|im_start|>assistant" in text:
        # Split and get everything after the assistant marker
        parts = text.split("<|im_start|>assistant")
        if len(parts) > 1:
            response = parts[-1]
            # Remove end markers
            response = response.replace("<|im_end|>", "").strip()
            return response
    
    # Fallback: use the original cleaning
    return clean_model_output(text)

def clean_model_output(text: str) -> str:
    """Clean the output from instruction-following models."""
    # Remove instruction tokens for both formats
    text = text.replace("<s>", "").replace("</s>", "")
    text = text.replace("[INST]", "").replace("[/INST]", "")
    text = text.replace("<|im_start|>", "").replace("<|im_end|>", "")
    
    # Split by common delimiters to find the actual response
    lines = text.split('\n')
    
    # Look for the assistant's response after the prompt
    clean_lines = []
    
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and system tokens
        if not line or line in ['user', 'assistant']:
            continue
            
        # Skip lines that look like instructions
        if any(starter in line.lower() for starter in [
            'write a creative', 'write a captivating', 'based on this story', 'describe the setting',
            'provide a detailed', 'create a detailed', 'create an immersive',
            'write exactly', 'write 4-5', 'requirements:', 'include:', 'focus on'
        ]):
            continue
            
        # This is likely the actual response
        clean_lines.append(line)
    
    # Join and clean up
    result = ' '.join(clean_lines)
    
    # Remove any remaining instruction artifacts
    result = re.sub(r"['\"]?\s*Create a detailed.*?memorable\.\s*", "", result)
    result = re.sub(r"['\"]?\s*Create an immersive.*?world\.\s*", "", result)
    result = re.sub(r"['\"]?\s*Write.*?sentences.*?\.\s*", "", result)
    result = re.sub(r"['\"]?\s*Requirements:.*?\]\s*", "", result)
    
    return result.strip()

def load_llm():
    # Using Qwen2.5-3B-Instruct - excellent quality, no auth required, fully open
    model_name = "Qwen/Qwen2.5-3B-Instruct"
    
    # Check if CUDA is available and set device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=350,
        min_new_tokens=80,
        repetition_penalty=1.1,
        do_sample=True,
        temperature=0.8,
        top_p=0.9,
        top_k=50,
        pad_token_id=tokenizer.eos_token_id
    )

    return HuggingFacePipeline(pipeline=pipe)

def generate_story_bundle(user_prompt: str):
    """Generate story, character, and background in one modern RunnableParallel pipeline."""
    llm = load_llm()

    # Step 1: Prompt for story
    story_prompt = PromptTemplate.from_template(
        "<|im_start|>user\n"
        "Write a captivating and creative short story about: {topic}\n\n"
        "Requirements:\n"
        "- 180-250 words\n"
        "- Rich narrative with compelling characters\n"
        "- Vivid descriptions and engaging dialogue\n"
        "- Complete story arc with beginning, middle, and satisfying end\n"
        "- Creative and original plot\n\n"
        "Focus on bringing the characters and world to life with immersive details.\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

    # Step 2: Prompt for character description
    character_prompt = PromptTemplate.from_template(
        "<|im_start|>user\n"
        "Based on this story:\n\n{story}\n\n"
        "Create a detailed character profile for the main character. Include:\n"
        "- Physical appearance (height, build, distinctive features, clothing/costume)\n"
        "- Personality traits, quirks, and mannerisms\n"
        "- Special abilities, skills, or powers\n"
        "- Background, motivations, and what drives them\n"
        "- How they speak and think\n\n"
        "Write 4-5 engaging sentences that make this character feel real and memorable.\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

    # Step 3: Prompt for background description
    background_prompt = PromptTemplate.from_template(
        "<|im_start|>user\n"
        "Based on this story:\n\n{story}\n\n"
        "Create an immersive setting description. Include:\n"
        "- Specific location details (architecture, landmarks, geography)\n"
        "- Time period, season, and weather\n"
        "- Atmosphere, mood, and emotional tone\n"
        "- Sensory details (sounds, smells, textures, lighting)\n"
        "- How the environment influences the story\n\n"
        "Write 4-5 vivid sentences that transport the reader into this world.\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

    # Build pipeline
    story_chain = story_prompt | llm | StrOutputParser()
    
    # First, generate the story
    story_text = story_chain.invoke({"topic": user_prompt})
    
    # Then generate character and background descriptions based on the story
    character_chain = character_prompt | llm | StrOutputParser()
    background_chain = background_prompt | llm | StrOutputParser()
    
    character_text = character_chain.invoke({"story": story_text})
    background_text = background_chain.invoke({"story": story_text})

    return {
        "story": clean_repetitive_text(extract_clean_response(story_text.strip())),
        "character": clean_repetitive_text(extract_clean_response(character_text.strip())),
        "background": clean_repetitive_text(extract_clean_response(background_text.strip()))
    }
