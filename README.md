# 📚 StorySmith AI

🤖 **AI-Powered Interactive Storytelling Platform**

An advanced AI system that transforms simple text prompts into rich, visual storytelling experiences using cutting-edge language models and image generation technology.

## 🌟 **What is StorySmith AI?**

StorySmith AI is a comprehensive platform that generates complete story visualizations from user prompts. It combines:

- **🎭 Story Generation**: Creative narratives using Hugging Face Transformers (Phi-3, GPT-2, etc.)
- **👤 Character Creation**: Detailed character descriptions and visualizations  
- **🖼️ Background Design**: Atmospheric scene descriptions and images
- **🎨 Image Composition**: AI-powered background removal (REMBG) and image merging
- **🌐 Web Interface**: Professional Django-based user interface with async processing

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

---

**Ready to create amazing AI-powered stories?** Choose your preferred implementation path and follow the detailed guides! 🚀