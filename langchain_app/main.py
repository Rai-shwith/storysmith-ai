"""
Main entry point for StorySmith AI LangChain application
"""

import os
import sys
import argparse
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chains.story_chain import create_story_chain
from utils.error_handler import log_info, log_error, StorySmithError
from config import OUTPUT_DIR


def generate_simple_story(topic: str) -> dict:
    """Simple story generation - just text, no images"""
    try:
        log_info(f"Starting story generation for topic: {topic}")
        
        print("� Generating story content...")
        
        # Use our working functional story chain
        story_chain = create_story_chain()
        story_result = story_chain.invoke({"topic": topic})
        story_data = story_result["result"]
        
        # Display results
        print("\n" + "="*50)
        print("GENERATED STORY")
        print("="*50)
        print(story_data["story"])
        print("\n" + "="*50)
        print("CHARACTER DESCRIPTION")
        print("="*50)
        print(story_data["character_description"])
        print("\n" + "="*50)
        print("BACKGROUND DESCRIPTION")
        print("="*50)
        print(story_data["background_description"])
        print("="*50 + "\n")
        
        # Prepare final result
        from datetime import datetime
        result = {
            "topic": topic,
            "story": story_data["story"],
            "character_description": story_data["character_description"],
            "background_description": story_data["background_description"],
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"\n🎉 STORY GENERATION COMPLETED! 🎉")
        
        return result
        
    except Exception as e:
        error_msg = f"Story generation failed: {e}"
        log_error(error_msg)
        raise StorySmithError(error_msg)


def main():
    """Main function with simplified interface"""
    parser = argparse.ArgumentParser(description="StorySmith AI - Generate creative stories")
    parser.add_argument("topic", nargs="?", help="The topic for story generation")
    parser.add_argument("--test", action="store_true", help="Run in test mode with predefined topic")
    
    args = parser.parse_args()
    
    try:
        if args.test:
            topic = "A magical adventure in an enchanted forest"
            print(f"Running in test mode with topic: {topic}")
        elif args.topic:
            topic = args.topic
        else:
            # Interactive mode
            print("Welcome to StorySmith AI!")
            print("Generate creative stories with character and background descriptions.")
            print("-" * 60)
            topic = input("Enter a topic for your story: ").strip()
            
            if not topic:
                print("No topic provided. Exiting.")
                return
        
        # Generate the story (simple approach)
        result = generate_simple_story(topic)
        
        # Save result summary
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = os.path.join(OUTPUT_DIR, f"story_summary_{timestamp}.txt")
        
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(f"StorySmith AI - Story Generation Summary\n")
            f.write(f"Generated on: {result['timestamp']}\n")
            f.write(f"Topic: {result['topic']}\n\n")
            f.write(f"STORY:\n{result['story']}\n\n")
            f.write(f"CHARACTER:\n{result['character_description']}\n\n")
            f.write(f"BACKGROUND:\n{result['background_description']}\n")
        
        print(f"\nSummary saved to: {summary_file}")
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except StorySmithError as e:
        print(f"StorySmith Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        log_error("Unexpected error in main", e)


if __name__ == "__main__":
    main()
