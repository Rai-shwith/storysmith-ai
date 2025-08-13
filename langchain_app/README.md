# StorySmith AI - Modern LangChain Application

A creative story generation application built with **LangChain 0.2+** modern architecture, combi## 📦 **Dependencies (Ultra-Lightweight)**

```bash
# LangChain Core - MINIMAL SETUP
langchain==0.2.1              # Core framework only
langchain-core==0.2.3         # Core abstractions

# Direct API calls - No deprecated endpoints
requests==2.31.0              # Direct HTTP calls to HuggingFace API

# Supporting libraries
Pillow==10.2.0                # Image processing  
python-dotenv==1.0.0          # Environment vars
colorama==0.4.6               # Terminal colors
```

**Ultra-Lightweight Approach:** This setup uses only LangChain's core components and direct API calls, avoiding ALL deprecated endpoints and heavy dependencies. Maximum efficiency!rfaces with Hugging Face APIs to generate stories, character descriptions, and merged visualizations.

## 🚀 **Modern LangChain Features**

- **🔗 Runnable Interface**: Built with LangChain's latest Runnable architecture for better composition
- **🏗️ Composite Chains**: Advanced chain orchestration using modern LangChain patterns  
- **📡 Streaming Support**: Real-time intermediate results streaming
- **🔄 Chain Composition**: Leverages LangChain's pipe operator (`|`) for elegant workflows
- **🎯 Type Safety**: Modern input/output typing with LangChain Core

## 📋 Prerequisites

- Python 3.8+
- Hugging Face account and API token
- Modern LangChain environment

## 🛠️ Installation

1. **Install lightweight dependencies:**
   ```bash
   cd langchain_app
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your HUGGINGFACE_API_TOKEN or HUGGINGFACEHUB_API_TOKEN
   ```

3. **Verify setup:**
   ```bash
   python test_setup.py
   ```

4. **Run your first story:**
   ```bash
   python main.py --test
   ```

## 🎯 Usage

### Modern Composite Chain (Recommended)

```bash
# Use modern LangChain composite chain
python main.py "A space explorer's journey"

# With streaming for real-time updates
python main.py "A magical quest" --stream
```

### Individual Chains (Legacy)

```bash
# Use individual chains
python main.py "A detective story" --legacy
```

### Test Modes

```bash
# Test with predefined topic
python main.py --test

# Test image generation only  
python main.py --test-images
```

## 🏗️ **Modern LangChain Architecture**

### Core Components

```
langchain_app/
├── chains/
│   ├── story_chain.py          # Runnable for story generation
│   ├── image_prompt_chain.py   # Runnable for prompt optimization  
│   └── composite_chain.py      # Composite chain orchestration
├── utils/
│   ├── image_merge.py          # Image processing pipeline
│   └── error_handler.py        # Enhanced error handling
└── main.py                     # Modern CLI with streaming
```

### Chain Composition

```python
from langchain_core.runnables import Runnable

# Modern LangChain pattern
class StoryChain(Runnable):
    def invoke(self, input_data):
        # Modern invoke method
        return {"result": processed_data}
        
# Composite chain orchestration
class StoryVisualizationChain(Runnable):
    def invoke(self, input_data):
        # Chain multiple runnables
        story_result = self.story_chain.invoke(input_data)
        prompt_result = self.prompt_chain.invoke(story_result)
        return final_result
```

## 🔧 **LangChain Integration Features**

### 1. **Runnable Interface**
- All chains implement LangChain's `Runnable` base class
- Consistent `invoke()` method for execution
- Support for streaming with `stream()` method

### 2. **Advanced Chain Composition**
```python
# Future: Pipe operator composition
chain = prompt_template | llm | output_parser

# Current: Composite chain orchestration  
composite_chain = StoryVisualizationChain()
result = composite_chain.invoke({"topic": "adventure"})
```

### 3. **Streaming Support**
```python
# Real-time progress updates
for update in chain.stream({"topic": "mystery"}):
    print(f"Step: {update['step']}, Status: {update['status']}")
```

### 4. **Direct HuggingFace API Integration**
```python
import requests

# Ultra-lightweight direct API calls
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2",
    headers=headers,
    json={"inputs": prompt, "parameters": {"max_new_tokens": 512}}
)
```

## � **Dependencies (Lightweight & Fast)**

```bash
# Modern LangChain stack - LIGHTWEIGHT FOR API USAGE
langchain==0.2.1              # Core framework
langchain-core==0.2.3         # Core abstractions  
langchain-community==0.2.1    # Community integrations (replaces langchain-huggingface)

# Lightweight HuggingFace API client (no heavy NVIDIA dependencies)
huggingface_hub==0.23.4       # API client only

# Supporting libraries
requests==2.31.0              # API calls
Pillow==10.2.0                # Image processing  
python-dotenv==1.0.0          # Environment vars
```

**Why Lightweight?** This setup avoids downloading heavy NVIDIA/PyTorch dependencies that come with `langchain-huggingface`, making installation much faster and lighter for API-only usage.

## 🎨 **Workflow**

1. **Topic Input** → `StoryChain` (Runnable)
2. **Story Generation** → `ImagePromptChain` (Runnable)  
3. **Prompt Optimization** → Image Generation Pipeline
4. **Image Synthesis** → Background Removal & Merging
5. **Final Output** → Story + Visualization

## � **Modern vs Legacy**

| Feature | Modern (Runnable) | Legacy (Chain) |
|---------|------------------|----------------|
| Interface | `invoke()` | `__call__()` |
| Composition | Pipe operators | Manual chaining |
| Streaming | Built-in | Custom |
| Type Safety | Full | Limited |
| Future-proof | ✅ | ❌ |

## � **Switching to Local GPU Models**

The modern architecture makes it easy to switch to local models:

```python
# In config.py
USE_LOCAL_MODELS = True

# Chains automatically adapt:
if USE_LOCAL_MODELS:
    # Use local transformers
else:
    # Use HuggingFace API
```

## 🤝 **Django Integration**

```python
# Modern Django integration
from langchain_app.chains.composite_chain import create_story_visualization_chain

def generate_story_view(request):
    chain = create_story_visualization_chain()
    result = chain.invoke({"topic": request.POST['topic']})
    return JsonResponse(result)
```

This modern LangChain application provides a solid foundation for building complex AI workflows with the latest tools and patterns!
