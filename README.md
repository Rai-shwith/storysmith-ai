# 📚 StorySmith AI

🤖 **AI-Powered Interactive Storytelling Platform**

An advanced AI system that transforms simple text prompts into rich, visual storytelling experiences using cutting-edge language models and image generation technology.

![StorySmith AI Interface](django_app/static/homepage.png)

## 🌟 **What is StorySmith AI?**

StorySmith AI is a comprehensive platform that generates complete story visualizations from user prompts. It combines:

- **🎭 Story Generation**: Creative narratives using Hugging Face Transformers (Phi-3, GPT-2, etc.)
- **👤 Character Creation**: Detailed character descriptions and visualizations  
- **🖼️ Background Design**: Atmospheric scene descriptions and images
- **🎨 Image Composition**: AI-powered background removal (REMBG) and image merging
- **🌐 Web Interface**: Professional Django-based user interface with async processing

## 🖼️ **Sample Output Showcase**

### **Example: "Deadpool in a fairy world"**

**📖 Generated Story:**
In the heart of an enchanted forest where trees whispered secrets to those who dared listen, there lived a peculiar character known as Wade Wilson. But he wasn't your average inhabitant; no, this was Fairytown—a realm untouched by time or sorrow. Here, magic reigned supreme, granting wishes that even mortals could only dream of. Yet amidst all its wonder stood one man whose presence seemed out of place yet oddly fitting - Deadpool.

Deadpool had stumbled upon this mystical land during his quest for eternal life when fate led him through a portal hidden beneath moonlit leaves. With each step into Fairytown, skepticism turned to amazement at how vibrant everything appeared compared to Earth's monochrome reality. The air shimmered like liquid silver around him while talking flowers offered cryptic advice on navigating their whimsical customs.

One day, Queen Celestia summoned Deadpool before her court – wizards donning robes made from spider silk floated above them holding crystal goblets filled with bubbling potions. "We require aid," she declared gravely. A dragon named Smolderwing terrorized nearby villages, leaving nothing but ash behind after every attack. Without hesitation, Deadpool sprang forth onto Cloud Nine, engaging in battle against fiery breath and razor talons until finally emerging victorious. His laughter echoed across valleys as villagers celebrated their newfound hero. And so it happened that Deadpool found himself not just surviving among fairies but thriving within these magical bounds forevermore.

**👤 Character Description:**
Standing tall with sharp features accentuated by angular lines running down his face, Deadpool sports tattered leather armor adorned with intricate patterns reflective of ancient battles won. Clad head-to-toe except for exposed hands gripping weapons carved from mythril, his eyes glint mischievously over half-moon spectacles perched precariously near his nose. Each movement is calculated, muscles rippling subtly underneath weathered skin hinting at countless skirmishes fought side by side with adversaries both human and supernatural alike.. transparent background, PNG format.

**🏞️ Background Description:**
[Ancient Enchanted Forest] As twilight embraces the skyline painted with hues of dusky purple and deepening blue, ethereal luminescence filters through towering canopies adorned with bioluminescent flora casting dancing lights below. Majestic ancient oaks stand guard over cobblestone pathways lined with iridescent stones leading towards a grand castle perched high amongst gnarled branches, exuding elegance despite centuries passed. Faint whispers carry along gentle wind currents carrying hints of spring blossoms intermingling with autumn chill, setting the stage for tales both old and timeless — Realistic/Cinematic Style Image Prompt.

### **🎨 Visual Pipeline Results**

| Stage | Image | Description |
|-------|-------|-------------|
| **1. Character Generation** | ![Character](langchain_app/outputs/character.jpeg) | SDXL-generated character based on story description |
| **2. Background Removal** | ![Character No BG](langchain_app/outputs/character_after_rembg.png) | AI-processed character with background removed using REMBG |
| **3. Background Generation** | ![Background](langchain_app/outputs/background.jpeg) | SDXL-generated enchanted forest background |
| **4. Final Composition** | ![Final Result](langchain_app/outputs/merged_output.jpg) | Character merged with background for complete visualization |

### **✨ Pipeline Highlights**
- **🎭 Rich Storytelling**: Complete narrative with character development and world-building
- **🎨 Precise Image Generation**: SDXL models create high-quality visuals matching story context
- **🔪 Clean Background Removal**: REMBG technology ensures seamless character extraction
- **🖼️ Professional Composition**: Intelligent merging creates cohesive final visualizations

## 🔧 **System Architecture**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Django Web    │    │   LangChain     │    │  HuggingFace    │
│   Interface     │───▶│   Pipeline      │───▶│  Transformers   │
│   (Frontend)    │    │   (Backend)     │    │  (AI Models)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### **🔄 Complete Story Generation Pipeline**

```
[User Topic Input] 
        │
        ▼
[Django Backend Processing]
        │
        ▼
[LangChain Pipeline Start]
        │
        ▼
[Story Generation]
(Phi-3/GPT-2 Models)
        │
        ▼
[Character & Background Description Generation]
        │
        ▼
[Prompt Enhancement & Optimization]
        │
    ┌───┴───┐
    ▼       ▼
[Character   [Background
 Image Gen]   Image Gen]
 (SDXL)       (SDXL)
    │           │
    ▼           ▼
[Background   [Background
 Removal]      Ready]
 (REMBG)
    │           │
    └─────┬─────┘
          ▼
[Character + Background Composition]
          │
          ▼
[Complete Story Package]
(Story Text + Final Image)
          │
          ▼
[Django Frontend Display]
```

### **🔄 Detailed Pipeline Flow**

1. **📝 User Input**: User submits topic through Django web interface
2. **🔄 Backend Processing**: Django creates async job and starts LangChain pipeline
3. **📚 Story Generation**: Hugging Face Transformers (Phi-3/GPT-2) generates complete story
4. **👤 Character Description**: AI extracts and enhances character details from story
5. **🏞️ Background Description**: AI creates atmospheric scene descriptions
6. **✨ Prompt Enhancement**: Story elements optimized into detailed image prompts
7. **🎨 Character Image**: SDXL model generates character portrait from enhanced prompt
8. **🖼️ Background Image**: SDXL model creates atmospheric background scene
9. **✂️ Background Removal**: REMBG processes character image to remove background
10. **🎭 Image Composition**: Character placed onto generated background scene
11. **📱 Result Display**: Complete story package shown in Django frontend

## 🚀 **Quick Start**

### **Prerequisites**
- Python 3.8+
- HuggingFace API Token (for Transformers models)
- Optional: GPU for enhanced local model performance

### **Choose Your Implementation**

#### **🌐 Django Web Interface** (Recommended)
```bash
cd django_app/
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Visit: http://127.0.0.1:8000/

#### **⚡ LangChain CLI** 
```bash
cd langchain_app/
pip install -r requirements.txt
python main.py
```

## 📁 **Project Structure**

```
storysmith-ai/
├── README.md                    # 📍 YOU ARE HERE - Project overview
├── Structure.md                 # Detailed architecture documentation
├── LICENSE                      # Project license
│
├── 🌐 django_app/              # Web interface implementation
│   ├── README.md               # 📖 Django-specific documentation
│   ├── manage.py               # Django management
│   ├── requirements.txt        # Django dependencies
│   ├── main/                   # Django app with async LangChain integration
│   │   ├── models.py          # Database models (StoryGenerationJob)
│   │   ├── views.py           # Async views with threading
│   │   ├── langchain_integration.py  # LangChain pipeline integration
│   │   └── templates/         # Professional UI templates
│   └── media/                  # Generated images and uploads
│
├── ⚡ langchain_app/           # Core AI pipeline implementation  
│   ├── README.md               # 📖 LangChain-specific documentation
│   ├── main.py                 # CLI interface
│   ├── requirements.txt        # AI/ML dependencies
│   ├── config.py               # Configuration management
│   ├── chains/                 # LangChain pipeline components
│   │   ├── story_chain.py     # Story generation logic
│   │   ├── image_prompt_chain.py  # Image prompt creation
│   │   └── composite_chain.py # Complete pipeline orchestration
│   ├── utils/                  # Utility modules
│   │   ├── error_handler.py   # Comprehensive error management
│   │   └── image_merge.py     # AI image composition
│   └── outputs/                # Generated stories and images
│
└── 📓 colab/                   # Google Colab notebooks
    ├── storysmith_colab_notebook.md
    └── image_gen_colab.ipynb
```

## ✨ **Key Features**

### **🎨 AI-Powered Story Generation**
- **Natural Language Processing**: Advanced prompt understanding using Hugging Face Transformers
- **Character Development**: Rich character personalities, appearances, and backgrounds
- **Scene Creation**: Detailed environmental descriptions and atmospheric settings
- **Narrative Structure**: Coherent storytelling with proper pacing and flow

### **🖼️ Visual Story Composition**
- **Character Visualization**: AI-generated character portraits using SDXL models
- **Background Synthesis**: Environmental scenes that match story atmosphere
- **Background Removal**: Intelligent character isolation using REMBG technology
- **Image Composition**: Professional character placement on AI-generated backgrounds

### **🌐 Professional Web Interface**
- **Async Processing**: Non-blocking 7-10 minute story generation with real-time updates
- **Progress Tracking**: Live status updates with auto-refreshing pages
- **Error Recovery**: Graceful failure handling with retry functionality
- **Media Management**: Organized storage and serving of generated content
- **Responsive Design**: Mobile-friendly interface with Bootstrap integration

### **🛡️ Production-Ready Architecture**
- **Local Model Support**: Full offline execution with downloaded Transformers models
- **API Integration**: Alternative cloud-based processing via HuggingFace API calls
- **Database Integration**: Job tracking with UUID-based identification
- **Threading System**: Background processing for long-running AI operations  
- **Error Handling**: Comprehensive error recovery and user feedback
- **Security Features**: CSRF protection, input validation, and secure file handling

## 🎯 **Use Cases**

- **📚 Creative Writing**: Generate story ideas and character concepts
- **🎮 Game Development**: Create character backstories and world-building content
- **📖 Educational Content**: Interactive storytelling for learning platforms
- **🎨 Art Projects**: Visual story concepts for illustrations and animations
- **🎭 Entertainment**: Personalized story experiences and interactive narratives

## 🔗 **Implementation Guides**

### **📖 For Django Web Development**
👉 **See: [`./django_app/README.md`](./django_app/README.md)**

Comprehensive guide covering:
- ✅ Complete Django setup and installation
- ✅ Async LangChain integration architecture  
- ✅ Database models and job tracking
- ✅ Auto-refreshing UI with progress indicators
- ✅ Error handling and retry mechanisms
- ✅ Production deployment considerations

### **📖 For LangChain AI Implementation**  
👉 **See: [`./langchain_app/README.md`](./langchain_app/README.md)**

Detailed documentation including:
- ✅ LangChain pipeline architecture
- ✅ AI model configuration and API setup
- ✅ Story generation chains and prompt engineering
- ✅ Image processing and composition techniques
- ✅ Error handling and logging systems
- ✅ Performance optimization and debugging

## 🔧 **Configuration**

### **🤖 AI Models Used**

StorySmith AI leverages state-of-the-art models from HuggingFace:

- **📝 Text Generation**: [`microsoft/Phi-3-mini-4k-instruct`](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) - Primary model for story generation and character descriptions
- **🎨 Image Generation**: [`stabilityai/stable-diffusion-xl-base-1.0`](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) - High-quality SDXL for character and background image creation

### **Environment Variables** (Required)
```bash
# In langchain_app/.env
HUGGINGFACE_API_TOKEN=your_huggingface_token

# Model Configuration (Optional - defaults provided)
TEXT_GENERATION_MODEL=microsoft/Phi-3-mini-4k-instruct
IMAGE_GENERATION_MODEL=stabilityai/stable-diffusion-xl-base-1.0
USE_LOCAL_MODELS=true

# Performance Settings
OUTPUT_DIR=./outputs
TEMP_DIR=./temp
LOG_FILE=storysmith.log
```

### **API Key Setup**
1. **HuggingFace**: Create token at [HuggingFace Settings](https://huggingface.co/settings/tokens)
2. **Alternative**: Can use HuggingFace API calls instead of local models (set `USE_LOCAL_MODELS=false`)

## 🧪 **Testing & Development**

### **Quick Test (No API Keys Required)**
```bash
# Test Django interface without LangChain
cd django_app/
python manage.py runserver
# Visit http://127.0.0.1:8000/ - graceful error handling demonstration
```

### **Full Integration Test**
```bash
# Test complete pipeline with HuggingFace models
cd langchain_app/
python test_pipeline.py
```

## 🚀 **Deployment Options**

- **🖥️ Local Development**: Full local execution with Hugging Face Transformers
- **☁️ Cloud Deployment**: Django app with HuggingFace API calls for scalability  
- **📓 Colab Integration**: Jupyter notebooks for experimentation and testing
- **🐳 Docker**: Containerized deployment with GPU support (configuration available)

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Follow the implementation guides in the respective README files
4. Test both Django and LangChain components
5. Submit a pull request with detailed descriptions

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 **Next Steps**

1. **Start with Django**: [`cd django_app/`](./django_app/) for the web interface
2. **Explore LangChain**: [`cd langchain_app/`](./langchain_app/) for AI implementation details  
3. **Check Examples**: [`cd colab/`](./colab/) for Jupyter notebook demonstrations

## 📋 **Development Status**

### **✅ Completed Features**
- ✅ Complete story generation pipeline with Hugging Face Transformers
- ✅ Character and background image generation using SDXL models
- ✅ Background removal and image composition with REMBG
- ✅ Professional Django web interface with async processing
- ✅ Real-time job tracking and progress updates
- ✅ Comprehensive error handling and retry mechanisms

### **🔄 Pending Features**
- 🔄 **Audio Integration**: Voice input processing and audio-based story generation (in development)

---

**Ready to create amazing AI-powered stories?** Choose your preferred implementation path and follow the detailed guides! 🚀