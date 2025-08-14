#!/usr/bin/env python3
"""
Test script for Enhanced StorySmith AI Pipeline
Tests the complete integration of story generation with image generation
"""

import os
import sys
import time
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_app.chains.story_chain import create_enhanced_story_chain, create_simple_story_chain
from utils.error_handler import log_info, log_error, log_warning
from config import USE_LOCAL_MODELS, OUTPUT_DIR

# Get logger for this module
logger = logging.getLogger(__name__)


def test_story_only():
    """Test story generation without images"""
    logger.info("🧪 Test 1: Story Generation Only")
    logger.info("=" * 50)
    
    try:
        simple_chain = create_simple_story_chain()
        
        test_topic = "A robot discovers emotions in a post-apocalyptic world"
        logger.info(f"Topic: {test_topic}")
        
        start_time = time.time()
        result = simple_chain.invoke({"topic": test_topic})
        end_time = time.time()
        
        story_result = result["result"]
        
        logger.info(f"\\n✅ Story generated in {end_time - start_time:.2f} seconds")
        logger.info(f"📖 Story length: {len(story_result['story'])} characters")
        logger.info(f"👤 Character: {story_result['character_description'][:100]}...")
        logger.info(f"🏞️  Background: {story_result['background_description'][:100]}...")
        
        return True
        
    except Exception as e:
        log_error(f"❌ Test failed: {e}")
        return False


def test_enhanced_chain():
    """Test the enhanced chain"""
    logger.info("\n🧪 Test 2: Enhanced Chain")
    logger.info("=" * 50)
    
    try:
        enhanced_chain = create_enhanced_story_chain(generate_images=False)  # No images for faster testing
        
        test_topic = "A magical library where books come alive"
        logger.info(f"Topic: {test_topic}")
        
        start_time = time.time()
        result = enhanced_chain.invoke({"topic": test_topic})
        end_time = time.time()
        
        if result:
            logger.info(f"\n✅ Enhanced chain completed in {end_time - start_time:.2f} seconds")
            logger.info(f"📖 Story length: {len(result['story'])} characters")
            logger.info(f"🎭 Detected style: {result.get('detected_style', 'None')}")
            return True
        else:
            log_error("❌ No result received")
            return False
            
    except Exception as e:
        log_error(f"❌ Test failed: {e}")
        return False


def test_image_integration():
    """Test the complete pipeline with image generation (if enabled)"""
    logger.info("\\n🧪 Test 3: Complete Pipeline with Images")
    logger.info("=" * 50)
    
    if not USE_LOCAL_MODELS:
        log_warning("⏭️  Skipping image test - USE_LOCAL_MODELS is disabled")
        log_info("   Enable local models in config.py to test image generation")
        return True
    
    try:
        enhanced_chain = create_enhanced_story_chain(generate_images=True)
        
        test_topic = "A small dragon learning to fly"
        logger.info(f"Topic: {test_topic}")
        logger.info("\\nThis may take several minutes with image generation...")
        
        start_time = time.time()
        result = enhanced_chain.invoke({"topic": test_topic})
        end_time = time.time()
        
        story_result = result["result"]
        
        logger.info(f"\\n✅ Complete pipeline finished in {end_time - start_time:.2f} seconds")
        logger.info(f"📖 Story: {len(story_result['story'])} characters")
        logger.info(f"🎭 Style: {story_result.get('detected_style', 'None')}")
        
        if story_result.get('final_image_path'):
            logger.info(f"🖼️  Final image: {story_result['final_image_path']}")
            logger.info(f"👤 Character image: {story_result.get('character_image_path', 'None')}")
            logger.info(f"🏞️  Background image: {story_result.get('background_image_path', 'None')}")
        else:
            log_warning("⚠️  No images generated")
        
        return True
        
    except Exception as e:
        log_error(f"❌ Test failed: {e}")
        import traceback
        log_error(traceback.format_exc())
        return False


def test_prompt_optimization():
    """Test just the prompt optimization chain"""
    logger.info("\\n🧪 Test 4: Image Prompt Optimization")
    logger.info("=" * 50)
    
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
        
        logger.info(f"✅ Prompt optimization successful")
        logger.info(f"🎭 Detected style: {image_prompts['detected_style']}")
        logger.info(f"👤 Character prompt: {image_prompts['character_prompt'][:100]}...")
        logger.info(f"🏞️  Background prompt: {image_prompts['background_prompt'][:100]}...")
        
        return True
        
    except Exception as e:
        log_error(f"❌ Test failed: {e}")
        return False


def main():
    """Run all tests"""
    logger.info("🚀 StorySmith AI Enhanced Pipeline Tests")
    logger.info("=" * 60)
    logger.info(f"📁 Output directory: {OUTPUT_DIR}")
    logger.info(f"🖼️  Local models enabled: {USE_LOCAL_MODELS}")
    logger.info("=" * 60)
    
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
            log_error(f"❌ Test {test_func.__name__} crashed: {e}")
            results.append(False)
        
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    logger.info("\\n" + "="*60)
    logger.info("📊 TEST SUMMARY")
    logger.info("="*60)
    
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
        logger.info(f"{i+1}. {name}: {status}")
    
    logger.info(f"\\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Enhanced pipeline is working correctly.")
    else:
        log_warning("⚠️  Some tests failed. Check the error messages above.")
    
    logger.info("\n🔗 Try the enhanced main script:")
    logger.info("   python enhanced_main.py --test")
    logger.info("   python enhanced_main.py --story-only 'Your topic here'")
    logger.info("   python enhanced_main.py 'Your topic here'")


if __name__ == "__main__":
    main()
