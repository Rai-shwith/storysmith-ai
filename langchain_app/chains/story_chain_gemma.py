from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
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

def clean_model_output(text: str) -> str:
    """Clean the output from instruction-following models."""
    # Remove special tokens
    text = text.replace("<bos>", "").replace("<eos>", "")
    text = text.replace("<start_of_turn>", "").replace("<end_of_turn>", "")
    
    # Split by lines and clean
    lines = text.split('\n')
    clean_lines = []
    for line in lines:
        line = line.strip()
        if line and not line.startswith(('user', 'model', 'Based on', 'Write a', 'Describe', 'Provide')):
            clean_lines.append(line)
    
    if clean_lines:
        return ' '.join(clean_lines)
    return text.strip()

def load_llm():
    # Using Gemma-2-2b-it - Google's lightweight but powerful model
    model_name = "google/gemma-2-2b-it"
    
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
        max_new_tokens=300,
        min_new_tokens=50,
        repetition_penalty=1.1,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        top_k=50,
        pad_token_id=tokenizer.eos_token_id
    )

    return HuggingFacePipeline(pipeline=pipe)

def generate_story_bundle(user_prompt: str):
    """Generate story, character, and background."""
    llm = load_llm()

    # Step 1: Prompt for story
    story_prompt = PromptTemplate.from_template(
        "<start_of_turn>user\nWrite a creative and engaging short story based on: {topic}. "
        "Create a complete narrative with interesting characters, vivid descriptions, and a compelling plot. "
        "Make it around 150-200 words. Be creative and original.<end_of_turn>\n<start_of_turn>model\n"
    )

    # Step 2: Prompt for character description
    character_prompt = PromptTemplate.from_template(
        "<start_of_turn>user\nBased on this story: '{story}' "
        "Provide a detailed description of the main character including their physical appearance, "
        "personality traits, background, and motivations. Write 3-4 sentences.<end_of_turn>\n<start_of_turn>model\n"
    )

    # Step 3: Prompt for background description
    background_prompt = PromptTemplate.from_template(
        "<start_of_turn>user\nBased on this story: '{story}' "
        "Describe the setting and atmosphere in detail including the location, time period, "
        "mood, and environmental details. Write 3-4 sentences.<end_of_turn>\n<start_of_turn>model\n"
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
        "story": clean_repetitive_text(clean_model_output(story_text.strip())),
        "character": clean_repetitive_text(clean_model_output(character_text.strip())),
        "background": clean_repetitive_text(clean_model_output(background_text.strip()))
    }
