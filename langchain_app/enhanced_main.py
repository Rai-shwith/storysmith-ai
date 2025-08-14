"""
Enhanced Main Entry Point for StorySmith AI
Integrates story generation with image generation in a complete LangChain pipeline
"""

import os
import sys
import argparse
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chains.enhanced_story_chain import create_enhanced_story_chain, create_simple_story_chain
from utils.error_handler import log_info, log_error, StorySmithError
from config import OUTPUT_DIR, USE_LOCAL_MODELS


def display_story_result(result: dict):
    """Display the generated story and image information in a nice format"""
    print("\n" + "="*70)
    print("🎉 STORYSMITH AI - COMPLETE STORY GENERATION 🎉")
    print("="*70)
    
    print(f"📝 Topic: {result['topic']}")
    print(f"🕒 Generated: {result['timestamp']}")
    if result.get('detected_style'):
        print(f"🎭 Style: {result['detected_style']}")
    
    print("\n" + "📖 STORY:")
    print("-" * 40)
    print(result['story'])
    
    print("\n" + "👤 CHARACTER DESCRIPTION:")
    print("-" * 40)
    print(result['character_description'])
    
    print("\n" + "🏞️ BACKGROUND DESCRIPTION:")
    print("-" * 40)
    print(result['background_description'])
    
    if result.get('character_prompt'):
        print("\n" + "🎨 IMAGE PROMPTS:")
        print("-" * 40)
        print(f"Character: {result['character_prompt']}")
        print(f"Background: {result['background_prompt']}")
    
    if result.get('final_image_path'):
        print("\n" + "🖼️ GENERATED IMAGES:")
        print("-" * 40)
        print(f"Character Image: {result['character_image_path']}")
        print(f"Background Image: {result['background_image_path']}")
        print(f"Final Merged Image: {result['final_image_path']}")
    
    print("\n" + "="*70)


def generate_story_with_images(topic: str) -> dict:
    """Generate story with complete image visualization"""
    try:
        log_info(f"Starting complete story generation with images for: {topic}")
        
        # Create the enhanced chain
        enhanced_chain = create_enhanced_story_chain(generate_images=True)
        
        # Run the complete pipeline
        result = enhanced_chain.invoke({"topic": topic})
        
        return result
        
    except Exception as e:
        error_msg = f"Enhanced story generation failed: {e}"
        log_error(error_msg)
        raise StorySmithError(error_msg)


def generate_story_only(topic: str) -> dict:
    """Generate story content only, no images"""
    try:
        log_info(f"Starting story-only generation for: {topic}")
        
        # Create simple chain without images
        simple_chain = create_simple_story_chain()
        
        # Run story generation only
        result = simple_chain.invoke({"topic": topic})
        
        return result
        
    except Exception as e:
        error_msg = f"Story generation failed: {e}"
        log_error(error_msg)
        raise StorySmithError(error_msg)


def main():
    """Enhanced main function with story and image generation modes"""
    parser = argparse.ArgumentParser(
        description="StorySmith AI - Enhanced Story Generation with Images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python enhanced_main.py "A magical adventure"           # Full generation
  python enhanced_main.py --story-only "Space adventure"  # Story only, no images
  python enhanced_main.py --test                          # Test mode
        """
    )
    
    parser.add_argument("topic", nargs="?", help="The topic for story generation")
    parser.add_argument("--story-only", action="store_true", 
                       help="Generate story content only (faster, no images)")
    parser.add_argument("--test", action="store_true", 
                       help="Run test with predefined topic")
    
    args = parser.parse_args()
    
    try:
        # Determine topic
        if args.test:
            topic = "A magical adventure in an enchanted forest with dragons"
            print(f"🧪 Running in test mode with topic: {topic}")
        elif args.topic:
            topic = args.topic
        else:
            # Interactive mode
            print("🎭 Welcome to StorySmith AI - Enhanced Edition!")
            print("Generate creative stories with optional image visualization.")
            print("-" * 60)
            topic = input("Enter a topic for your story: ").strip()
            
            if not topic:
                print("No topic provided. Exiting.")
                return
        
        # Check if image generation is available
        if not USE_LOCAL_MODELS and not args.story_only:
            print("⚠️  Note: Local models disabled. Consider using --story-only for faster generation.")
            user_choice = input("Continue with full generation? (y/n): ").strip().lower()
            if user_choice != 'y':
                args.story_only = True
        
        # Generate based on mode
        if args.story_only:
            print("\n📝 Generating story content only...")
            result = generate_story_only(topic)
        else:
            print("\n🎨 Generating complete story with images...")
            result = generate_story_with_images(topic)
        
        # Display results
        display_story_result(result)
        
        # Save summary (if not already saved by enhanced chain)
        if args.story_only:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_file = os.path.join(OUTPUT_DIR, f"story_only_summary_{timestamp}.txt")
            
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(f"StorySmith AI - Story Only Summary\n")
                f.write(f"Generated on: {result['timestamp']}\n")
                f.write(f"Topic: {result['topic']}\n\n")
                f.write(f"STORY:\n{result['story']}\n\n")
                f.write(f"CHARACTER:\n{result['character_description']}\n\n")
                f.write(f"BACKGROUND:\n{result['background_description']}\n")
            
            print(f"\n📄 Summary saved to: {summary_file}")
        
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user.")
    except StorySmithError as e:
        print(f"\n❌ StorySmith Error: {e}")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        log_error("Unexpected error in enhanced main", e)


if __name__ == "__main__":
    main()
