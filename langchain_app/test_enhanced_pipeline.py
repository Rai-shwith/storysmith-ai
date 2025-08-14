#!/usr/bin/env python3
"""
Test script for Enhanced StorySmith AI Pipeline
Tests the complete integration of story generation with image generation
"""

import os
import sys
import time

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chains.enhanced_story_chain import create_enhanced_story_chain, create_simple_story_chain
from utils.error_handler import log_info
from config import USE_LOCAL_MODELS, OUTPUT_DIR


def test_story_only():
    """Test story generation without images"""
    print("🧪 Test 1: Story Generation Only")
    print("=" * 50)
    
    try:
        simple_chain = create_simple_story_chain()
        
        test_topic = "A robot discovers emotions in a post-apocalyptic world"
        print(f"Topic: {test_topic}")
        
        start_time = time.time()
        result = simple_chain.invoke({"topic": test_topic})
        end_time = time.time()
        
        story_result = result["result"]
        
        print(f"\\n✅ Story generated in {end_time - start_time:.2f} seconds")
        print(f"📖 Story length: {len(story_result['story'])} characters")
        print(f"👤 Character: {story_result['character_description'][:100]}...")
        print(f"🏞️  Background: {story_result['background_description'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_enhanced_chain():
    """Test the enhanced chain"""
    print("\n🧪 Test 2: Enhanced Chain")
    print("=" * 50)
    
    try:
        enhanced_chain = create_enhanced_story_chain(generate_images=False)  # No images for faster testing
        
        test_topic = "A magical library where books come alive"
        print(f"Topic: {test_topic}")
        
        start_time = time.time()
        result = enhanced_chain.invoke({"topic": test_topic})
        end_time = time.time()
        
        if result:
            print(f"\n✅ Enhanced chain completed in {end_time - start_time:.2f} seconds")
            print(f"📖 Story length: {len(result['story'])} characters")
            print(f"🎭 Detected style: {result.get('detected_style', 'None')}")
            return True
        else:
            print("❌ No result received")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_image_integration():
    """Test the complete pipeline with image generation (if enabled)"""
    print("\\n🧪 Test 3: Complete Pipeline with Images")
    print("=" * 50)
    
    if not USE_LOCAL_MODELS:
        print("⏭️  Skipping image test - USE_LOCAL_MODELS is disabled")
        print("   Enable local models in config.py to test image generation")
        return True
    
    try:
        enhanced_chain = create_enhanced_story_chain(generate_images=True)
        
        test_topic = "A small dragon learning to fly"
        print(f"Topic: {test_topic}")
        print("\\nThis may take several minutes with image generation...")
        
        start_time = time.time()
        result = enhanced_chain.invoke({"topic": test_topic})
        end_time = time.time()
        
        story_result = result["result"]
        
        print(f"\\n✅ Complete pipeline finished in {end_time - start_time:.2f} seconds")
        print(f"📖 Story: {len(story_result['story'])} characters")
        print(f"🎭 Style: {story_result.get('detected_style', 'None')}")
        
        if story_result.get('final_image_path'):
            print(f"🖼️  Final image: {story_result['final_image_path']}")
            print(f"👤 Character image: {story_result.get('character_image_path', 'None')}")
            print(f"🏞️  Background image: {story_result.get('background_image_path', 'None')}")
        else:
            print("⚠️  No images generated")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_prompt_optimization():
    """Test just the prompt optimization chain"""
    print("\\n🧪 Test 4: Image Prompt Optimization")
    print("=" * 50)
    
    try:
        from chains.image_prompt_chain import create_image_prompt_chain
        
        prompt_chain = create_image_prompt_chain()
        
        # Create test story data
        test_story_data = {
            "story": "A brave knight ventured into the dark mystical forest where ancient magic still lingered among the towering trees.",
            "character_description": "A young knight in shining silver armor, wielding a glowing sword, with determination in their eyes",
            "background_description": "A mysterious forest with ancient oak trees, glowing mushrooms, and wisps of magical energy floating in the air"
        }
        
        result = prompt_chain.invoke({"story_data": test_story_data})
        image_prompts = result["image_prompts"]
        
        print(f"✅ Prompt optimization successful")
        print(f"🎭 Detected style: {image_prompts['detected_style']}")
        print(f"👤 Character prompt: {image_prompts['character_prompt'][:100]}...")
        print(f"🏞️  Background prompt: {image_prompts['background_prompt'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 StorySmith AI Enhanced Pipeline Tests")
    print("=" * 60)
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print(f"🖼️  Local models enabled: {USE_LOCAL_MODELS}")
    print("=" * 60)
    
    tests = [
        test_story_only,
        test_enhanced_chain,
        test_prompt_optimization,
        test_image_integration
    ]
    
    results = []
    
    for test_func in tests:
        try:
            success = test_func()
            results.append(success)
        except Exception as e:
            print(f"❌ Test {test_func.__name__} crashed: {e}")
            results.append(False)
        
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    test_names = [
        "Story Generation Only",
        "Enhanced Chain", 
        "Image Prompt Optimization",
        "Complete Pipeline with Images"
    ]
    
    passed = sum(results)
    total = len(results)
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{i+1}. {name}: {status}")
    
    print(f"\\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced pipeline is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
    
    print("\n🔗 Try the enhanced main script:")
    print("   python enhanced_main.py --test")
    print("   python enhanced_main.py --story-only 'Your topic here'")
    print("   python enhanced_main.py 'Your topic here'")


if __name__ == "__main__":
    main()
