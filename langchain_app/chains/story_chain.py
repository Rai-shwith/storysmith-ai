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

def enforce_png_format(text: str) -> str:
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

def load_llm():
    # Using Phi-3-mini-4k-instruct - smaller but very capable model
    model_name = "microsoft/Phi-3-mini-4k-instruct"

    # Check if CUDA is available and set device
    device = "cuda" if torch.cuda.is_available() else "cpu"

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True,
        attn_implementation="eager"  # Use eager attention to avoid cache issues
    )

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=400,  # Increased further to prevent truncation
        min_new_tokens=60,
        repetition_penalty=1.1,
        do_sample=True,
        temperature=0.7,
        top_p=0.9,
        top_k=50,
        pad_token_id=tokenizer.eos_token_id,
        use_cache=False  # Disable caching to avoid the seen_tokens issue
    )

    return HuggingFacePipeline(pipeline=pipe)

def generate_story_bundle(user_prompt: str):
    """Generate story, character, and background."""
    llm = load_llm()

    # Step 1: Prompt for story
    story_prompt = PromptTemplate.from_template(
        "<|user|>\n"
        "Write a creative short story about: {topic}\n"
        "Requirements:\n"
        "- 150-200 words\n"
        "- Complete narrative with beginning, middle, end\n"
        "- Vivid descriptions and unique characters\n"
        "- Action and dialogue\n"
        "<|end|>\n<|assistant|>\n"
    )

    # Step 2: Enhanced character description prompt
    character_prompt = PromptTemplate.from_template(
        "<|user|>\n"
        "You are an AI prompt generator for image models.\n"
        "From this story:\n\n{story}\n\n"
        "Generate ONLY a short, visual description of the MAIN CHARACTER.\n"
        "Strict rules:\n"
        "1. Focus only on visible physical traits, clothing, accessories, body language, facial expression.\n"
        "2. No background elements.\n"
        "3. No camera settings or photography jargon.\n"
        "4. Write in ONE paragraph under 80 words.\n"
        "5. End EXACTLY with: 'transparent background, PNG format'.\n"
        "6. Do not add anything else.\n\n"
        "OUTPUT FORMAT:\n"
        "<description sentence(s)>. transparent background, PNG format\n"
        "<|end|>\n<|assistant|>\n"
    )


    # Step 3: Enhanced background description → Image prompt for AI generation
    background_prompt = PromptTemplate.from_template(
        "<|user|>\n"
        "You are an AI prompt generator for background images.\n"
        "Based on this story:\n\n{story}\n\n"
        "Create a concise, highly visual prompt for the SETTING of the story.\n"
        "Guidelines:\n"
        "- Describe only the environment and scenery, without including any characters or creatures.\n"
        "- Include specific location details, architecture, and landmarks relevant to the story.\n"
        "- Indicate time of day, season, and weather.\n"
        "- Convey atmosphere and mood visually (e.g., lighting, color tone) rather than poetically.\n"
        "- Ensure composition is wide enough to place a character in the scene later.\n"
        "- Keep it under 3 sentences.\n"
        "- End with the desired style (realistic, cinematic, anime, etc.).\n"
        "- Background does not need to be transparent.\n\n"
        "Final format:\n"
        "A detailed image prompt, ending with style keywords.\n"
        "<|end|>\n<|assistant|>\n"
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
        "character": enforce_png_format(clean_repetitive_text(extract_clean_response(character_text.strip()))),
        "background": clean_repetitive_text(extract_clean_response(background_text.strip()))
    }

def generate_story_bundle_with_images(user_prompt: str, generate_images: bool = True, 
                                    save_directory: str = "/content/drive/MyDrive/storysmith_images/"):
    """Generate complete story bundle with optional image generation."""
    # Generate text content first
    print("=== GENERATING STORY CONTENT ===")
    story_bundle = generate_story_bundle(user_prompt)
    
    print("\n=== STORY GENERATED ===")
    print("Story:", story_bundle["story"][:100] + "...")
    print("Character prompt:", story_bundle["character"])
    print("Background prompt:", story_bundle["background"])
    
    if generate_images:
        try:
            from .image_prompt_chain import generate_story_images
            print("\n=== STARTING IMAGE GENERATION ===")
            image_results = generate_story_images(story_bundle, save_directory)
            story_bundle.update(image_results)
            print("✅ Images generated successfully!")
        except Exception as e:
            print(f"❌ Image generation failed: {e}")
            print("Continuing with text-only results...")
    
    return story_bundle
