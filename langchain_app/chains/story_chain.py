from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnablePassthrough

def load_llm():
    model_name = "google/flan-t5-large"  
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=150,
        min_new_tokens=50,
        repetition_penalty=1.8,
        do_sample=True,
        temperature=0.8,
        top_p=0.95,
        top_k=50
    )

    return HuggingFacePipeline(pipeline=pipe)

def generate_story_bundle(user_prompt: str):
    """Generate story, character, and background in one modern RunnableParallel pipeline."""
    llm = load_llm()

    # Step 1: Prompt for story
    story_prompt = PromptTemplate.from_template(
        "Write a concise, original short story about {topic}. "
        "Avoid repeating phrases. Limit to 120 words."
    )

    # Step 2: Prompt for character description
    character_prompt = PromptTemplate.from_template(
        "From the following story, give a vivid, unique description of the main character "
        "(appearance, personality, and role). Avoid repeating sentences. Under 80 words.\n\n{story}"
    )

    # Step 3: Prompt for background description
    background_prompt = PromptTemplate.from_template(
        "From the following story, describe the setting and background in detail "
        "(time period, location, mood). Avoid repeating phrases. Under 80 words.\n\n{story}"
    )

    # Build pipeline
    story_chain = story_prompt | llm | StrOutputParser()

    # Parallel branches for character & background using story output
    parallel_chains = RunnableParallel(
        story=story_chain,
        character=RunnablePassthrough() | character_prompt | llm | StrOutputParser(),
        background=RunnablePassthrough() | background_prompt | llm | StrOutputParser()
    )

    # First, generate story
    story_text = story_chain.invoke({"topic": user_prompt})

    # Then, run character + background in parallel using the story text
    final_result = parallel_chains.invoke({"story": story_text, "topic": user_prompt})

    return {
        "story": story_text.strip(),
        "character": final_result["character"].strip(),
        "background": final_result["background"].strip()
    }
