# storysmith-ai/langchain_app/main.py

from chains.story_chain import generate_story_bundle
from utils.error_handler import log_error

if __name__ == "__main__":
    try:
        user_prompt = input("Enter your story idea: ")
        result = generate_story_bundle(user_prompt)
        print("\n=== STORY ===")
        print(result["story"])
        print("\n=== CHARACTER DESCRIPTION ===")
        print(result["character"])
        print("\n=== BACKGROUND DESCRIPTION ===")
        print(result["background"])
    except Exception as e:
        log_error(e)
