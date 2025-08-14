# StorySmith AI - LangChain Pipeline

🎭 **AI-Powered Story Generation with Visual Storytelling**

A sophisticated LangChain-based pipeline that transforms simple text prompts into complete story visualizations, combining advanced language models with AI-powered image generation and processing.

## 🎯 **Project Overview**

StorySmith AI creates immersive story experiences by:
- **Story Generation**: Crafting engaging narratives with detailed character and background descriptions
- **Prompt Engineering**: Optimizing descriptions for high-quality image generation
- **Visual Creation**: Generating character and background images using SDXL
- **AI Background Removal**: Using `rembg` for precise character extraction
- **Image Composition**: Merging characters and backgrounds into cohesive visualizations

## 🏗️ **Architecture & LangChain Flow**

### **Complete Pipeline Architecture**

```mermaid
graph TD
    A[📝 Topic Input] --> B[🧠 Story Chain]
    B --> C[📖 Story + Character + Background Descriptions]
    C --> D[🎨 Image Prompt Chain]
    D --> E[✨ Optimized Image Prompts]
    E --> F[🖼️ Character Image Generation]
    E --> G[🖼️ Background Image Generation]
    F --> H[🤖 AI Background Removal - rembg]
    G --> I[🔗 Image Merging Pipeline]
    H --> I
    I --> J[🎉 Final Story Visualization]
```

### **LangChain Components**

#### 1. **EnhancedStoryVisualizationChain** (`chains/story_chain.py`)
**Main orchestrator implementing `langchain_core.runnables.Runnable`**

```python
class EnhancedStoryVisualizationChain(Runnable):
    """
    Complete LangChain pipeline that:
    1. Generates story content (story, character desc, background desc)
    2. Optimizes descriptions into image prompts  
    3. Generates character and background images
    4. Removes backgrounds using AI (rembg)
    5. Merges images into final visualization
    """
```

**Pipeline Flow:**
- **Step 1**: Story content generation using existing story chain
- **Step 2**: Image prompt optimization for SDXL compatibility
- **Step 3**: Parallel character and background image generation
- **Step 4**: AI-powered background removal from character images
- **Step 5**: Intelligent image merging and composition
- **Step 6**: Summary generation and file management

#### 2. **Image Prompt Chain** (`chains/image_prompt_chain.py`)
**LangChain Runnable for prompt optimization**

- **Style Detection**: Analyzes story content to determine artistic style
- **Prompt Enhancement**: Optimizes character/background descriptions for SDXL
- **Template Application**: Uses configurable prompt templates
- **Quality Assurance**: Ensures prompts meet image generation requirements

#### 3. **Story Chain** (existing component)
**Leverages existing story generation capabilities with enhanced integration**

## 🤖 **Models & Technologies**

### **AI Models Used**

| Component | Model | Purpose | Provider |
|-----------|-------|---------|----------|
| **Text Generation** | `microsoft/Phi-3-mini-4k-instruct` | Story and description generation | Microsoft |
| **Image Generation** | `stabilityai/stable-diffusion-xl-base-1.0` | High-quality image creation | Stability AI |
| **Background Removal** | `rembg` (U²-Net) | AI-powered background extraction | Open Source |

### **Technical Stack**

- **LangChain**: Orchestration and pipeline management
- **Transformers**: Local model execution
- **Diffusers**: SDXL pipeline implementation
- **rembg**: AI background removal
- **Pillow**: Image processing and manipulation
- **PyTorch**: Deep learning framework

## 📁 **Project Structure**

```
langchain_app/
├── main.py                     # Main entry point (was enhanced_main.py)
├── test_pipeline.py            # Comprehensive testing suite
├── config.py                   # Configuration and model settings
├── requirements.txt            # Dependencies with rembg
├── chains/                     # LangChain components
│   ├── story_chain.py          # Main orchestration chain
│   ├── image_prompt_chain.py   # Prompt optimization
│   └── composite_chain.py      # Legacy integration
├── utils/                      # Utility modules
│   ├── error_handler.py        # Robust error handling & logging
│   └── image_merge.py          # AI background removal & merging
├── outputs/                    # Generated content
│   ├── *.jpg                   # Final story visualizations
│   └── *.txt                   # Story summaries
└── temp/                       # Temporary processing files
```

## 🚀 **Quick Start**

### **1. Prerequisites**

```bash
# Python 3.8+ required
python --version

# GPU support (optional but recommended)
nvidia-smi  # Check CUDA availability
```

### **2. Installation**

```bash
# Navigate to langchain_app directory
cd langchain_app

# Install dependencies (includes rembg)
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Hugging Face token (if using API)
```

### **3. Configuration**

#### **Local Models (Recommended)**
```python
# config.py
USE_LOCAL_MODELS = True  # Use local SDXL and Phi-3
TEXT_GENERATION_MODEL = "microsoft/Phi-3-mini-4k-instruct"
IMAGE_GENERATION_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
```

#### **API Usage (Alternative)**
```bash
# Set Hugging Face token
export HUGGINGFACE_API_TOKEN="your_hf_token_here"
```

### **4. Usage Examples**

#### **Command Line Interface**

```bash
# Test the complete pipeline
python main.py --test

# Story generation only (fast)
python main.py --story-only "A robot discovers emotions"

# Full generation with images
python main.py "A magical library where books come alive"

# Interactive mode
python main.py
```

#### **Programmatic Usage**

```python
from chains.story_chain import create_enhanced_story_chain

# Complete pipeline with images
chain = create_enhanced_story_chain(generate_images=True)
result = chain.invoke({"topic": "A dragon learning to fly"})

# Access results
print(f"Story: {result['story']}")
print(f"Final Image: {result['final_image_path']}")
print(f"Style Detected: {result['detected_style']}")

# Story-only mode for fast generation
story_chain = create_enhanced_story_chain(generate_images=False)
story_result = story_chain.invoke({"topic": "A space adventure"})
```

## 🎨 **Prompt Engineering Integration**

The system employs sophisticated prompt engineering techniques:

### **Multi-Stage Prompt Optimization**
1. **Story Analysis**: Extracting key narrative elements
2. **Style Detection**: Identifying artistic direction
3. **Prompt Enhancement**: Optimizing for SDXL performance
4. **Quality Assurance**: Ensuring generation consistency

### **Template-Based Approach**
```python
CHARACTER_PROMPT_TEMPLATE = """
{character_description}, {style_modifier}, 
high quality, detailed, professional artwork, 
perfect anatomy, clear details
"""
```

*For detailed prompt engineering documentation, see [PROMPT_ENGINEERING.md](./PROMPT_ENGINEERING.md)*

## 🔧 **Advanced Features**

### **Flexible Execution Modes**
- **Full Pipeline**: Complete story + image generation
- **Story Only**: Fast text generation without images
- **Test Mode**: Quick validation with predefined topics

### **Robust Error Handling**
```python
class StorySmithError(Exception):
    """Custom exception with detailed error context"""
    
# Comprehensive logging throughout pipeline
logger.info("🎯 Starting Enhanced Story Generation Pipeline...")
logger.error("Image generation failed", exc_info=True)
```

### **Background Removal Intelligence**
```python
# AI-powered background removal with fallback
if REMBG_AVAILABLE:
    # Use rembg for AI-powered removal
    output_bytes = remove(image_bytes)
else:
    # Fallback to color-based removal
    fallback_removal(image)
```

## 🧪 **Testing & Validation**

### **Comprehensive Test Suite**

```bash
# Run all pipeline tests
python test_pipeline.py

# Individual component tests
python debug_image_prompt.py  # Prompt chain testing
python test_image_gen.py      # Image generation testing
```

### **Test Coverage**
- ✅ Story generation validation
- ✅ Prompt optimization testing
- ✅ Image generation pipeline
- ✅ Background removal accuracy
- ✅ End-to-end integration
- ✅ Error handling scenarios

## 📊 **Performance & Optimization**

### **Local vs API Performance**

| Mode | Story Generation | Image Generation | Total Time |
|------|------------------|------------------|------------|
| **Local Models** | ~10-30s | ~60-120s | ~2-3 minutes |
| **API (HF)** | ~5-15s | ~30-90s | ~1-2 minutes |

### **Memory Requirements**
- **SDXL Local**: 8GB+ VRAM recommended
- **Phi-3 Local**: 4GB+ RAM
- **rembg**: 2GB+ RAM

### **Optimization Features**
- Memory-efficient SDXL loading
- Attention slicing for lower VRAM
- Temporary file cleanup
- Background process management

## 🔍 **Evaluation Criteria Compliance**

### **✅ Prompt Engineering Creativity**
- Multi-stage prompt optimization
- Style-aware template system
- Comprehensive prompt documentation

### **✅ LangChain Orchestration**
- Complete `Runnable` implementation
- Modular chain composition
- Proper data flow management

### **✅ Narrative Quality**
- Phi-3 model for coherent storytelling
- Structured output format
- Character/background integration

### **✅ Visual Appeal**
- SDXL for high-quality images
- AI-powered background removal
- Professional image composition

### **✅ Code Robustness**
- Comprehensive error handling
- Detailed logging system
- Modular architecture

### **✅ Documentation Quality**
- Complete setup instructions
- Architecture documentation
- Prompt engineering guide

### **✅ Free/Open AI Tools**
- Microsoft Phi-3 (MIT License)
- Stability AI SDXL (Open License)
- rembg (MIT License)
- All dependencies are open source

## 🐛 **Troubleshooting**

### **Common Issues**

#### **CUDA/GPU Issues**
```bash
# Check CUDA availability
python -c "import torch; print(torch.cuda.is_available())"

# CPU fallback
# Set USE_LOCAL_MODELS=False in config.py
```

#### **rembg Installation**
```bash
# If rembg import fails
pip install rembg[gpu]  # For GPU support
# or
pip install rembg       # CPU only
```

#### **Model Download Issues**
```bash
# Clear cache and retry
huggingface-cli delete-cache
python main.py --test
```

## 📈 **Future Enhancements**

- [ ] Multi-language story generation
- [ ] Video generation integration
- [ ] Advanced style transfer options
- [ ] Interactive web interface improvements
- [ ] Real-time streaming capabilities

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Add comprehensive tests
4. Update documentation
5. Submit a pull request

## 📄 **License**

This project uses open-source AI models and is distributed under the MIT License.

---

*For detailed prompt engineering techniques and examples, see [PROMPT_ENGINEERING.md](./PROMPT_ENGINEERING.md)*