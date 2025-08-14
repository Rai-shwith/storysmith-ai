#!/usr/bin/env python3
"""
Simple test script to debug the image prompt chain issue
Tests with prefilled story data to isolate the problem
"""

import os
import sys
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chains.image_prompt_chain import create_image_prompt_chain
from utils.error_handler import log_info, log_error

# Get logger for this module
logger = logging.getLogger(__name__)


def test_image_prompt_chain():
    """Test the image prompt chain with known good data"""
    logger.info("🧪 Testing Image Prompt Chain with Prefilled Data")
    logger.info("=" * 60)
    
    # Create test story data that matches what story_chain should return
    test_story_data = {
        "story": "A brave farmer named John worked tirelessly in the fields of New York. Despite the urban sprawl around him, he maintained his small farm with love and dedication. One day, he discovered something magical hidden beneath the soil that would change his life forever.",
        "character_description": "A tall man named John stands proudly in overalls and a wide-brimmed hat, with weathered hands and kind eyes that show years of hard work and determination.",
        "background_description": "An expansive view of a rustic farm nestled within the bustling cityscape of New York, with green fields stretching toward skyscrapers in the distance."
    }
    
    logger.info("📝 Test story data:")
    logger.info(f"   Story: {test_story_data['story'][:100]}...")
    logger.info(f"   Character: {test_story_data['character_description'][:80]}...")
    logger.info(f"   Background: {test_story_data['background_description'][:80]}...")
    
    try:
        # Create the image prompt chain
        logger.info("\n🔗 Creating image prompt chain...")
        image_prompt_chain = create_image_prompt_chain()
        
        # Test the invoke method with the expected input format
        logger.info("\n🎨 Testing image prompt generation...")
        input_data = {"story_data": test_story_data}
        
        logger.info("📊 Input data structure:")
        logger.info(f"   Keys: {list(input_data.keys())}")
        logger.info(f"   story_data keys: {list(input_data['story_data'].keys())}")
        
        # Invoke the chain
        result = image_prompt_chain.invoke(input_data)
        
        logger.info("\n✅ SUCCESS! Image prompt chain worked!")
        logger.info("📋 Results:")
        image_prompts = result["image_prompts"]
        logger.info(f"   🎭 Detected style: {image_prompts['detected_style']}")
        logger.info(f"   👤 Character prompt: {image_prompts['character_prompt'][:100]}...")
        logger.info(f"   🏞️  Background prompt: {image_prompts['background_prompt'][:100]}...")
        
        return True
        
    except Exception as e:
        log_error(f"\n❌ FAILED! Error: {e}")
        logger.debug("\n🔍 Debug information:")
        logger.debug(f"   Exception type: {type(e)}")
        logger.debug(f"   Exception args: {e.args}")
        
        # Additional debugging
        import traceback
        logger.debug("\n📋 Full traceback:")
        log_error(traceback.format_exc())
        
        return False


def test_with_different_formats():
    """Test with different data formats to see what works"""
    logger.info("\n🧪 Testing Different Data Formats")
    logger.info("=" * 60)
    
    image_prompt_chain = create_image_prompt_chain()
    
    # Test format 1: Direct story data (what we expect)
    logger.info("\n📋 Test 1: Direct story data format")
    test_data_1 = {
        "story_data": {
            "story": "A simple test story about adventure.",
            "character_description": "A brave hero with a sword.",
            "background_description": "A mystical forest setting."
        }
    }
    
    try:
        result = image_prompt_chain.invoke(test_data_1)
        logger.info("   ✅ Format 1 worked!")
    except Exception as e:
        log_error(f"   ❌ Format 1 failed: {e}")
    
    # Test format 2: What if story_data is missing?
    logger.info("\n📋 Test 2: Missing story_data")
    test_data_2 = {
        "story": "A simple test story about adventure.",
        "character_description": "A brave hero with a sword.",
        "background_description": "A mystical forest setting."
    }
    
    try:
        result = image_prompt_chain.invoke(test_data_2)
        logger.info("   ✅ Format 2 worked!")
    except Exception as e:
        log_error(f"   ❌ Format 2 failed: {e}")
    
    # Test format 3: Empty data
    logger.info("\n📋 Test 3: Empty data")
    test_data_3 = {}
    
    try:
        result = image_prompt_chain.invoke(test_data_3)
        logger.info("   ✅ Format 3 worked!")
    except Exception as e:
        log_error(f"   ❌ Format 3 failed: {e}")


def test_story_chain_output():
    """Test what the actual story chain returns"""
    logger.info("\n🧪 Testing Actual Story Chain Output")
    logger.info("=" * 60)
    
    try:
        from chains.story_chain import create_story_chain
        
        story_chain = create_story_chain()
        
        logger.info("📝 Generating story with actual story chain...")
        story_result = story_chain.invoke({"topic": "a farmer in New York"})
        
        logger.info("📊 Story chain result structure:")
        logger.info(f"   Type: {type(story_result)}")
        logger.info(f"   Keys: {list(story_result.keys())}")
        
        if "result" in story_result:
            story_data = story_result["result"]
            logger.info(f"   Result type: {type(story_data)}")
            logger.info(f"   Result keys: {list(story_data.keys())}")
            
            # Now test with this actual data
            logger.info("\n🎨 Testing image prompt chain with actual story data...")
            image_prompt_chain = create_image_prompt_chain()
            
            result = image_prompt_chain.invoke({"story_data": story_data})
            logger.info("   ✅ SUCCESS with actual story chain data!")
            
        return True
        
    except Exception as e:
        log_error(f"   ❌ FAILED: {e}")
        import traceback
        log_error(traceback.format_exc())
        return False


def main():
    """Run all tests"""
    logger.info("🚀 Image Prompt Chain Debug Tests")
    logger.info("=" * 80)
    
    tests = [
        ("Basic Prefilled Test", test_image_prompt_chain),
        ("Different Formats Test", test_with_different_formats),
        ("Actual Story Chain Test", test_story_chain_output)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Running: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            log_error(f"❌ Test {test_name} crashed: {e}")
            results.append((test_name, False))
        
        logger.info("\n" + "-" * 80)
    
    # Summary
    logger.info("\n📊 TEST SUMMARY")
    logger.info("=" * 80)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        logger.info(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    logger.info(f"\n🎯 Overall: {passed}/{total} tests passed")


if __name__ == "__main__":
    main()
