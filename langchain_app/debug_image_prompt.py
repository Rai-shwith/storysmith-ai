#!/usr/bin/env python3
"""
Simple test script to debug the image prompt chain issue
Tests with prefilled story data to isolate the problem
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from chains.image_prompt_chain import create_image_prompt_chain


def test_image_prompt_chain():
    """Test the image prompt chain with known good data"""
    print("🧪 Testing Image Prompt Chain with Prefilled Data")
    print("=" * 60)
    
    # Create test story data that matches what story_chain should return
    test_story_data = {
        "story": "A brave farmer named John worked tirelessly in the fields of New York. Despite the urban sprawl around him, he maintained his small farm with love and dedication. One day, he discovered something magical hidden beneath the soil that would change his life forever.",
        "character_description": "A tall man named John stands proudly in overalls and a wide-brimmed hat, with weathered hands and kind eyes that show years of hard work and determination.",
        "background_description": "An expansive view of a rustic farm nestled within the bustling cityscape of New York, with green fields stretching toward skyscrapers in the distance."
    }
    
    print("📝 Test story data:")
    print(f"   Story: {test_story_data['story'][:100]}...")
    print(f"   Character: {test_story_data['character_description'][:80]}...")
    print(f"   Background: {test_story_data['background_description'][:80]}...")
    
    try:
        # Create the image prompt chain
        print("\n🔗 Creating image prompt chain...")
        image_prompt_chain = create_image_prompt_chain()
        
        # Test the invoke method with the expected input format
        print("\n🎨 Testing image prompt generation...")
        input_data = {"story_data": test_story_data}
        
        print("📊 Input data structure:")
        print(f"   Keys: {list(input_data.keys())}")
        print(f"   story_data keys: {list(input_data['story_data'].keys())}")
        
        # Invoke the chain
        result = image_prompt_chain.invoke(input_data)
        
        print("\n✅ SUCCESS! Image prompt chain worked!")
        print("📋 Results:")
        image_prompts = result["image_prompts"]
        print(f"   🎭 Detected style: {image_prompts['detected_style']}")
        print(f"   👤 Character prompt: {image_prompts['character_prompt'][:100]}...")
        print(f"   🏞️  Background prompt: {image_prompts['background_prompt'][:100]}...")
        
        return True
        
    except Exception as e:
        print(f"\n❌ FAILED! Error: {e}")
        print("\n🔍 Debug information:")
        print(f"   Exception type: {type(e)}")
        print(f"   Exception args: {e.args}")
        
        # Additional debugging
        import traceback
        print("\n📋 Full traceback:")
        traceback.print_exc()
        
        return False


def test_with_different_formats():
    """Test with different data formats to see what works"""
    print("\n🧪 Testing Different Data Formats")
    print("=" * 60)
    
    image_prompt_chain = create_image_prompt_chain()
    
    # Test format 1: Direct story data (what we expect)
    print("\n📋 Test 1: Direct story data format")
    test_data_1 = {
        "story_data": {
            "story": "A simple test story about adventure.",
            "character_description": "A brave hero with a sword.",
            "background_description": "A mystical forest setting."
        }
    }
    
    try:
        result = image_prompt_chain.invoke(test_data_1)
        print("   ✅ Format 1 worked!")
    except Exception as e:
        print(f"   ❌ Format 1 failed: {e}")
    
    # Test format 2: What if story_data is missing?
    print("\n📋 Test 2: Missing story_data")
    test_data_2 = {
        "story": "A simple test story about adventure.",
        "character_description": "A brave hero with a sword.",
        "background_description": "A mystical forest setting."
    }
    
    try:
        result = image_prompt_chain.invoke(test_data_2)
        print("   ✅ Format 2 worked!")
    except Exception as e:
        print(f"   ❌ Format 2 failed: {e}")
    
    # Test format 3: Empty data
    print("\n📋 Test 3: Empty data")
    test_data_3 = {}
    
    try:
        result = image_prompt_chain.invoke(test_data_3)
        print("   ✅ Format 3 worked!")
    except Exception as e:
        print(f"   ❌ Format 3 failed: {e}")


def test_story_chain_output():
    """Test what the actual story chain returns"""
    print("\n🧪 Testing Actual Story Chain Output")
    print("=" * 60)
    
    try:
        from chains.story_chain import create_story_chain
        
        story_chain = create_story_chain()
        
        print("📝 Generating story with actual story chain...")
        story_result = story_chain.invoke({"topic": "a farmer in New York"})
        
        print("📊 Story chain result structure:")
        print(f"   Type: {type(story_result)}")
        print(f"   Keys: {list(story_result.keys())}")
        
        if "result" in story_result:
            story_data = story_result["result"]
            print(f"   Result type: {type(story_data)}")
            print(f"   Result keys: {list(story_data.keys())}")
            
            # Now test with this actual data
            print("\n🎨 Testing image prompt chain with actual story data...")
            image_prompt_chain = create_image_prompt_chain()
            
            result = image_prompt_chain.invoke({"story_data": story_data})
            print("   ✅ SUCCESS with actual story chain data!")
            
        return True
        
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("🚀 Image Prompt Chain Debug Tests")
    print("=" * 80)
    
    tests = [
        ("Basic Prefilled Test", test_image_prompt_chain),
        ("Different Formats Test", test_with_different_formats),
        ("Actual Story Chain Test", test_story_chain_output)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {e}")
            results.append((test_name, False))
        
        print("\n" + "-" * 80)
    
    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 80)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\n🎯 Overall: {passed}/{total} tests passed")


if __name__ == "__main__":
    main()
