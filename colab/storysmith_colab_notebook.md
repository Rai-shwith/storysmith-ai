# StorySmith AI - Complete Story & Image Generation Pipeline

## 🚀 Setup (Run Once)

```python
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Install dependencies
!pip install diffusers==0.21.4 transformers==4.35.2 accelerate xformers langchain langchain-huggingface torch torchvision Pillow numpy

# Clone your repository (adjust the path as needed)
import os
os.chdir('/content/drive/MyDrive/')

# If you need to clone from GitHub:
# !git clone https://github.com/Rai-shwith/storysmith-ai.git
# os.chdir('/content/drive/MyDrive/storysmith-ai')

print("✅ Setup complete!")
```

## 📖 Generate Story + Images

```python
# Navigate to your project directory
import os
import sys
os.chdir('/content/drive/MyDrive/storysmith-ai')
sys.path.append('/content/drive/MyDrive/storysmith-ai')

# Import the main function
from langchain_app.main import main

# Run the complete pipeline
main()
```

## 🧪 Test Image Generation Only

```python
# Test just the image generation with a sample story
from langchain_app.chains.image_prompt_chain import generate_story_images

# Sample story bundle
test_story = {
    "story": "A brave wizard stands in an enchanted forest, casting magical spells.",
    "character": "A tall wizard wearing blue robes, holding a glowing staff, long white beard, pointed hat. transparent background, PNG format",
    "background": "Enchanted forest with glowing mushrooms, magical particles in the air, mystical atmosphere, fantasy landscape"
}

# Generate images
result = generate_story_images(test_story, "/content/drive/MyDrive/storysmith_images/test/")

print("Images generated!")
print(f"Character: {result['character_path']}")
print(f"Background: {result['background_path']}")
print(f"Final Scene: {result['merged_path']}")
```

## 🎨 View Generated Images

```python
from PIL import Image
import matplotlib.pyplot as plt

# Load and display images
def show_generated_images(base_path="/content/drive/MyDrive/storysmith_images/"):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    try:
        # Character image
        char_img = Image.open(f"{base_path}character.png")
        axes[0].imshow(char_img)
        axes[0].set_title("Character (Transparent)")
        axes[0].axis('off')
        
        # Background image
        bg_img = Image.open(f"{base_path}background.png")
        axes[1].imshow(bg_img)
        axes[1].set_title("Background")
        axes[1].axis('off')
        
        # Final merged image
        final_img = Image.open(f"{base_path}final_scene.png")
        axes[2].imshow(final_img)
        axes[2].set_title("Final Scene")
        axes[2].axis('off')
        
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f"Error loading images: {e}")

# Show the latest generated images
show_generated_images()
```

## 🛠️ Custom Story Generation

```python
# Generate with specific prompts
from langchain_app.chains.story_chain import generate_story_bundle_with_images

# Custom story idea
story_idea = "A ninja cat who fights crime in Tokyo at night"

# Generate everything
result = generate_story_bundle_with_images(
    story_idea, 
    generate_images=True,
    save_directory="/content/drive/MyDrive/storysmith_images/custom/"
)

print("=== GENERATED CONTENT ===")
print("Story:", result["story"])
print("Character:", result["character"])
print("Background:", result["background"])

if "merged_path" in result:
    print(f"✅ Images saved to: {result['merged_path']}")
```

## 📁 File Structure

Your Google Drive should have:
```
MyDrive/
├── storysmith-ai/           # Your project folder
│   ├── langchain_app/
│   │   ├── chains/
│   │   │   ├── story_chain.py
│   │   │   └── image_prompt_chain.py
│   │   └── main.py
│   └── colab_setup.py
└── storysmith_images/       # Generated images folder
    ├── character.png
    ├── background.png
    └── final_scene.png
```

## 🎯 Tips for Better Results

1. **Character Prompts**: Be specific about appearance, clothing, pose
2. **Background Prompts**: Include lighting, mood, architectural details
3. **Story Ideas**: More detailed stories = better image prompts
4. **Memory**: Restart runtime if you get CUDA out of memory errors

## 🔧 Troubleshooting

```python
# Check GPU availability
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")

# Clear GPU memory if needed
if torch.cuda.is_available():
    torch.cuda.empty_cache()
    print("GPU memory cleared")
```
