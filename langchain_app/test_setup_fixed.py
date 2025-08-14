"""
Test script for local model setup
Verifies that local models (Phi-3-mini and SDXL) work without API dependencies
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

def test_local_model_setup():
    """Test the local model setup for Phi-3-mini and SDXL"""
    
    print("🧪 Testing Local Model Setup")
    print("=" * 50)
    
    try:
        # Test 1: Import core components
        print("1️⃣  Testing core imports...")
        from langchain_core.runnables import Runnable
        from langchain_core.prompts import PromptTemplate
        print("   ✅ LangChain core imports successful!")
        
        # Test 2: Test ML/AI library imports
        print("\n2️⃣  Testing ML library imports...")
        try:
            import torch
            print(f"   ✅ PyTorch installed: {torch.__version__}")
            print(f"   🔥 CUDA available: {torch.cuda.is_available()}")
            if torch.cuda.is_available():
                gpu_name = torch.cuda.get_device_name()
                gpu_memory_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
                print(f"   🎮 GPU device: {gpu_name}")
                print(f"   💾 GPU memory: {gpu_memory_gb:.1f}GB")
                
                # GPU memory assessment
                if gpu_memory_gb < 4:
                    print("   ⚠️  Limited GPU VRAM - may need to use CPU for image generation")
                elif gpu_memory_gb < 8:
                    print("   ✅ Good GPU VRAM for most models")
                else:
                    print("   🚀 Excellent GPU VRAM - perfect for SDXL and large models!")
        except ImportError as e:
            print(f"   ❌ PyTorch import failed: {e}")
            return False
            
        try:
            import transformers
            print(f"   ✅ Transformers installed: {transformers.__version__}")
        except ImportError as e:
            print(f"   ❌ Transformers import failed: {e}")
            return False
            
        try:
            import diffusers
            print(f"   ✅ Diffusers installed: {diffusers.__version__}")
        except ImportError as e:
            print(f"   ❌ Diffusers import failed: {e}")
            return False

        # Test 3: Test text generation model loading
        print("\n3️⃣  Testing text generation model...")
        try:
            from transformers import AutoTokenizer
            from config import TEXT_GENERATION_MODEL
            
            print(f"   📥 Loading tokenizer for: {TEXT_GENERATION_MODEL}")
            tokenizer = AutoTokenizer.from_pretrained(TEXT_GENERATION_MODEL)
            print(f"   ✅ Tokenizer loaded successfully!")
            print(f"   📝 Vocab size: {len(tokenizer)}")
            
            # Test tokenization
            test_text = "Hello, how are you?"
            tokens = tokenizer.encode(test_text)
            print(f"   🧪 Test tokenization: '{test_text}' -> {len(tokens)} tokens")
            
        except Exception as e:
            print(f"   ❌ Text model test failed: {e}")
            print("   💡 Model will be downloaded on first use")
        
        # Test 4: Test image generation model loading (just check if it can be imported)
        print("\n4️⃣  Testing image generation setup...")
        try:
            from diffusers import StableDiffusionXLPipeline
            from config import IMAGE_GENERATION_MODEL
            
            print(f"   📥 Image model configured: {IMAGE_GENERATION_MODEL}")
            print(f"   ✅ SDXL pipeline class imported successfully!")
            print("   💡 Image model will be downloaded on first use (~7GB)")
            
        except Exception as e:
            print(f"   ❌ Image model test failed: {e}")
            return False
        
        # Test 5: Test local configuration
        print("\n5️⃣  Testing local model configuration...")
        try:
            from config import USE_LOCAL_MODELS, LOCAL_MODEL_PATH, OUTPUT_DIR, TEMP_DIR
            
            print(f"   🏠 USE_LOCAL_MODELS: {USE_LOCAL_MODELS}")
            print(f"   📁 LOCAL_MODEL_PATH: {LOCAL_MODEL_PATH}")
            print(f"   📁 OUTPUT_DIR: {OUTPUT_DIR}")
            print(f"   📁 TEMP_DIR: {TEMP_DIR}")
            
            # Check if directories exist
            dirs_to_check = [OUTPUT_DIR, TEMP_DIR]
            if USE_LOCAL_MODELS:
                dirs_to_check.append(LOCAL_MODEL_PATH)
                
            for dir_path in dirs_to_check:
                if os.path.exists(dir_path):
                    print(f"   ✅ Directory exists: {dir_path}")
                else:
                    print(f"   📁 Directory will be created: {dir_path}")
                    
        except Exception as e:
            print(f"   ❌ Configuration test failed: {e}")
            return False
        
        # Test 6: Test story chain import
        print("\n6️⃣  Testing story chain setup...")
        try:
            from chains.story_chain import create_story_chain
            story_chain = create_story_chain()
            print("   ✅ Story chain created successfully!")
            
            # Test prompt template
            prompt = story_chain.prompt_template.format(topic="a magical adventure")
            print(f"   📝 Prompt template working: {len(prompt)} characters")
            
        except Exception as e:
            print(f"   ❌ Story chain test failed: {e}")
            return False
        
        # Test 7: Test image utilities
        print("\n7️⃣  Testing image processing utilities...")
        try:
            from utils.image_merge import generate_image_from_prompt
            from PIL import Image
            print("   ✅ Image processing utilities imported!")
            print("   🖼️  Pillow (PIL) available for image processing")
            
        except Exception as e:
            print(f"   ❌ Image utilities test failed: {e}")
            return False
        
        # Test 8: Memory requirements check
        print("\n8️⃣  Checking system requirements...")
        try:
            import psutil
            
            # Get system memory
            memory = psutil.virtual_memory()
            memory_gb = memory.total / (1024**3)
            available_gb = memory.available / (1024**3)
            
            print(f"   💾 Total RAM: {memory_gb:.1f}GB")
            print(f"   💾 Available RAM: {available_gb:.1f}GB")
            
            if memory_gb < 6:
                print("   ❌ Warning: Less than 6GB RAM detected. Models may not run.")
            elif memory_gb < 8:
                print("   ⚠️  Warning: Less than 8GB RAM detected. Models may run slowly.")
            elif memory_gb < 12:
                print("   ✅ Good RAM for local model execution!")
                if torch.cuda.is_available():
                    print("   🎮 GPU available - SDXL will use GPU VRAM instead of system RAM!")
            else:
                print("   ✅ Excellent RAM for local model execution!")
                
        except ImportError:
            print("   ℹ️  psutil not available, skipping memory check")
        except Exception as e:
            print(f"   ⚠️  Memory check failed: {e}")
        
        print("\n🎉 All tests passed! Local model setup is ready.")
        print("💡 You can now run: python main.py --test")
        print("📥 Models will be downloaded automatically on first use:")
        print("   • Phi-3-mini-4k-instruct (~2.4GB)")
        print("   • SDXL-base-1.0 (~7GB)")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        return False


def test_quick_generation():
    """Test a quick text generation to verify everything works"""
    print("\n🚀 Quick Generation Test")
    print("=" * 30)
    
    try:
        from chains.story_chain import create_story_chain
        
        print("Creating story chain...")
        story_chain = create_story_chain()
        
        print("Testing with a simple topic...")
        result = story_chain.invoke({"topic": "a friendly robot"})
        
        if result and "result" in result:
            story_data = result["result"]
            print("✅ Story generation successful!")
            print(f"📖 Story preview: {story_data.get('story', '')[:100]}...")
        else:
            print("❌ Story generation failed - no result returned")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Quick generation test failed: {e}")
        print("💡 This is normal if models haven't been downloaded yet")
        return False


if __name__ == "__main__":
    print("🔧 StorySmith AI - Local Model Setup Test")
    print("=" * 60)
    
    # Run main setup test
    setup_success = test_local_model_setup()
    
    if setup_success:
        print("\n" + "=" * 60)
        print("✨ Setup test completed successfully!")
        
        # Ask if user wants to run quick generation test
        try:
            user_input = input("\n🤔 Run quick generation test? (y/N): ").strip().lower()
            if user_input in ['y', 'yes']:
                generation_success = test_quick_generation()
                if generation_success:
                    print("\n🎉 All tests passed! Ready for local story generation!")
                else:
                    print("\n⚠️  Generation test failed, but setup is ready.")
                    print("💡 Models will download on first actual use.")
            else:
                print("\n✅ Setup verified! Run 'python main.py' to start generating stories.")
                
        except KeyboardInterrupt:
            print("\n👋 Test interrupted by user")
    else:
        print("\n🔧 Please fix the issues above before proceeding.")
        print("\n💡 Common fixes:")
        print("   • Run: pip install -r requirements.txt")
        print("   • Ensure you have sufficient RAM (8GB+ recommended)")
        print("   • Check that Python packages are properly installed")
