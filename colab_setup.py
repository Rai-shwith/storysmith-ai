"""
Setup script for Google Colab - StorySmith AI Image Generation
Run this in Colab to install all dependencies and mount Google Drive
"""

def setup_colab_environment():
    """Complete setup for Colab environment."""
    
    print("🚀 Setting up StorySmith AI in Google Colab...")
    
    # Install required packages
    print("\n📦 Installing required packages...")
    import subprocess
    import sys
    
    packages = [
        "diffusers==0.21.4",
        "transformers==4.35.2", 
        "accelerate",
        "xformers",
        "langchain",
        "langchain-huggingface",
        "torch",
        "torchvision", 
        "torchaudio",
        "Pillow",
        "numpy"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("✅ All packages installed!")
    
    # Mount Google Drive
    print("\n💾 Mounting Google Drive...")
    try:
        from google.colab import drive
        drive.mount('/content/drive')
        print("✅ Google Drive mounted successfully!")
    except ImportError:
        print("⚠️  Not in Colab environment, skipping Drive mount")
    
    # Create directories
    print("\n📁 Creating directories...")
    import os
    
    directories = [
        "/content/drive/MyDrive/storysmith_images",
        "/content/drive/MyDrive/storysmith_backup"
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Created: {directory}")
        except:
            print(f"⚠️  Could not create: {directory}")
    
    print("\n🎉 Setup complete! You can now run StorySmith AI!")
    print("\nUsage:")
    print("from langchain_app.main import main")
    print("main()")

def quick_test():
    """Quick test of the image generation pipeline."""
    print("\n🧪 Running quick test...")
    
    try:
        from chains.image_prompt_chain import test_image_generation
        result = test_image_generation()
        print("✅ Test completed successfully!")
        return result
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None

if __name__ == "__main__":
    setup_colab_environment()
