from chains.story_chain import generate_story_bundle_with_images
from utils.error_handler import log_error

def main():
    """Main function to run the complete story + image generation pipeline."""
    try:
        user_prompt = input("Enter your story idea: ")
        
        # Ask if user wants images
        generate_images = input("Generate images? (y/n): ").lower().startswith('y')
        
        print("Generating story bundle...")
        result = generate_story_bundle_with_images(
            user_prompt, 
            generate_images=generate_images,
            save_directory="/content/drive/MyDrive/storysmith_images/"
        )

        print("\n" + "="*50)
        print("=== STORY ===")
        print(result["story"])

        print("\n=== CHARACTER DESCRIPTION ===")
        print(result["character"])

        print("\n=== BACKGROUND DESCRIPTION ===")
        print(result["background"])
        
        if generate_images and "character_path" in result:
            print(f"\n=== IMAGES GENERATED ===")
            print(f"📸 Character: {result['character_path']}")
            print(f"🖼️  Background: {result['background_path']}")
            print(f"🎬 Final Scene: {result['merged_path']}")
            print(f"\n✨ All images saved to Google Drive!")

    except Exception as e:
        log_error(e)
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
