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
from chains.image_prompt_chain import create_image_prompt_chain
from chains.composite_chain import create_story_visualization_chain
from utils.image_merge import create_story_visualization
from utils.error_handler import log_info, log_error, StorySmithError
from config import OUTPUT_DIR


def generate_complete_story(topic: str, use_composite_chain: bool = True) -> dict:
    """Complete pipeline to generate story and visualization"""
    try:
        log_info(f"Starting story generation for topic: {topic}")
        
        if use_composite_chain:
            # Use modern LangChain composite chain
            print("🔗 Using Modern LangChain Composite Chain")
            composite_chain = create_story_visualization_chain()
            result = composite_chain.invoke({"topic": topic})
            
            # Display results
            print("\n" + "="*50)
            print("GENERATED STORY")
            print("="*50)
            print(result["story"])
            print("\n" + "="*50)
            print("CHARACTER DESCRIPTION")
            print("="*50)
            print(result["character_description"])
            print("\n" + "="*50)
            print("BACKGROUND DESCRIPTION")
            print("="*50)
            print(result["background_description"])
            print("="*50 + "\n")
            
            print("OPTIMIZED IMAGE PROMPTS")
            print("="*50)
            print(f"Style: {result['detected_style']}")
            print(f"\nCharacter Prompt:\n{result['character_prompt']}")
            print(f"\nBackground Prompt:\n{result['background_prompt']}")
            print("="*50 + "\n")
            
            final_image_path = result["final_image_path"]
            
            # Add timestamp for consistency
            from datetime import datetime
            result["timestamp"] = datetime.now().isoformat()
            
        else:
            # Use individual chains (legacy approach)
            print("⛓️  Using Individual Chain Approach")
            
            # Step 1: Generate story, character, and background descriptions
            story_chain = create_story_chain()
            story_result = story_chain.invoke({"topic": topic})
            story_data = story_result["result"]
            
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
            
            # Step 2: Convert descriptions to optimized image prompts
            prompt_chain = create_image_prompt_chain()
            prompt_result = prompt_chain.invoke({"story_data": story_data})
            image_prompts = prompt_result["image_prompts"]
            
            print("OPTIMIZED IMAGE PROMPTS")
            print("="*50)
            print(f"Style: {image_prompts['detected_style']}")
            print(f"\nCharacter Prompt:\n{image_prompts['character_prompt']}")
            print(f"\nBackground Prompt:\n{image_prompts['background_prompt']}")
            print("="*50 + "\n")
            
            # Step 3: Generate and merge images
            story_title = topic.replace(" ", "_").lower()
            final_image_path = create_story_visualization(
                image_prompts["character_prompt"],
                image_prompts["background_prompt"],
                story_title
            )
            
            # Prepare final result
            from datetime import datetime
            result = {
                "topic": topic,
                "story": story_data["story"],
                "character_description": story_data["character_description"],
                "background_description": story_data["background_description"],
                "character_prompt": image_prompts["character_prompt"],
                "background_prompt": image_prompts["background_prompt"],
                "detected_style": image_prompts["detected_style"],
                "final_image_path": final_image_path,
                "timestamp": datetime.now().isoformat()
            }
        
        print(f"\n🎉 STORY GENERATION COMPLETED! 🎉")
        print(f"Final image saved to: {final_image_path}")
        print(f"Check the output directory: {OUTPUT_DIR}")
        
        return result
        
    except Exception as e:
        error_msg = f"Story generation pipeline failed: {e}"
        log_error(error_msg)
        raise StorySmithError(error_msg)


def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description="StorySmith AI - Generate creative stories with visualizations")
    parser.add_argument("topic", nargs="?", help="The topic for story generation")
    parser.add_argument("--test", action="store_true", help="Run in test mode with predefined topic")
    parser.add_argument("--test-images", action="store_true", help="Test image generation only")
    parser.add_argument("--legacy", action="store_true", help="Use individual chains instead of modern composite chain")
    parser.add_argument("--stream", action="store_true", help="Stream intermediate results (only works with composite chain)")
    
    args = parser.parse_args()
    
    try:
        if args.test_images:
            print("Testing image generation pipeline...")
            from utils.image_merge import test_image_generation
            test_image_generation()
            return
        
        if args.test:
            topic = "A magical adventure in an enchanted forest"
            print(f"Running in test mode with topic: {topic}")
        elif args.topic:
            topic = args.topic
        else:
            # Interactive mode
            print("Welcome to StorySmith AI!")
            print("Generate creative stories with character and background visualizations.")
            print("-" * 60)
            topic = input("Enter a topic for your story: ").strip()
            
            if not topic:
                print("No topic provided. Exiting.")
                return
        
        # Generate the complete story
        use_composite = not args.legacy
        if args.stream and use_composite:
            # Use streaming for real-time updates
            print("🌊 Using Streaming Mode with Composite Chain")
            composite_chain = create_story_visualization_chain()
            for update in composite_chain.stream({"topic": topic}):
                print(f"📡 {update['step']}: {update['status']}")
                if update['status'] == 'completed' and 'data' in update:
                    print(f"   ✅ Data received for {update['step']}")
                elif update['status'] == 'success':
                    result = update['result']
                    break
        else:
            result = generate_complete_story(topic, use_composite_chain=use_composite)
        
        # Save result summary
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        summary_file = os.path.join(OUTPUT_DIR, f"story_summary_{timestamp}.txt")
        
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write(f"StorySmith AI - Story Generation Summary\n")
            f.write(f"Generated on: {result['timestamp']}\n")
            f.write(f"Topic: {result['topic']}\n")
            f.write(f"Style: {result['detected_style']}\n\n")
            f.write(f"STORY:\n{result['story']}\n\n")
            f.write(f"CHARACTER:\n{result['character_description']}\n\n")
            f.write(f"BACKGROUND:\n{result['background_description']}\n\n")
            f.write(f"FINAL IMAGE: {result['final_image_path']}\n")
        
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
