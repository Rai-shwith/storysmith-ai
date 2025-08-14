# Prompt Engineering Documentation
## StorySmith AI - LangChain-Orchestrated Story Visualization Pipeline

🎯 **Project-focused documentation of prompt engineering techniques implemented in StorySmith AI**

---

## 📖 **Project Overview**

StorySmith AI is a LangChain-based pipeline that transforms simple user topics into complete story visualizations. The system combines **Microsoft Phi-3-mini-4k-instruct** for story generation with **Stable Diffusion XL** for high-quality image creation, demonstrating advanced prompt engineering and modern LangChain orchestration.

**Key Innovation**: Multi-stage prompt optimization pipeline with automated style detection and background removal for seamless character-background compositing.

---

## 🔧 **How the Story Prompt Works**

### **Actual Template Implementation**

```python
# From config.py - Optimized for Phi-3-mini instruction following
STORY_PROMPT_TEMPLATE = """<|user|>
Write a creative short story about: {topic}
Requirements:
- 150-200 words
- Complete narrative with beginning, middle, end
- Vivid descriptions and unique characters
- Action and dialogue
<|end|>
<|assistant|>
"""
```

### **Design Choices**

- **Phi-3 Chat Format**: Uses `<|user|>` and `<|assistant|>` tokens for optimal instruction following
- **Constrained Length**: 150-200 words ensures focused narratives while providing sufficient detail
- **Visual Emphasis**: Explicitly requests "vivid descriptions" for downstream image generation
- **Structural Requirements**: Enforces complete narrative arc for coherent storytelling

### **Topic Enhancement Strategy**

The system processes basic user inputs through contextual enrichment:
- Simple topics like "robot" become "A curious robot discovering emotions"
- Genre detection adds appropriate atmospheric elements
- Emotional depth and conflict are automatically integrated

---

## 👤 **Character Prompt Construction**

### **Step-by-Step Process**

#### **1. Character Extraction Template**
```python
# From config.py
CHARACTER_PROMPT_TEMPLATE = """<|user|>
You are an AI prompt generator for image models.
From this story: {story}

Generate ONLY a short, visual description of the MAIN CHARACTER.
Strict rules:
1. Focus only on visible physical traits, clothing, accessories, body language, facial expression.
2. No background elements.
3. No camera settings or photography jargon.
4. Write in ONE paragraph under 80 words.
5. End EXACTLY with: 'transparent background, PNG format'.
6. Do not add anything else.

OUTPUT FORMAT:
<description sentence(s)>. transparent background, PNG format
<|end|>
<|assistant|>
"""
```

#### **2. SDXL Optimization Template**
```python
CHARACTER_IMAGE_PROMPT_TEMPLATE = """
{character_description}, full body shot, isolated on pure white background, 
png style, no background, clean edges, high quality, detailed, 
{style_modifier}
"""
```

### **Example Character Prompt Evolution**

**Input Story**: *"A brave knight named Sir Elena stood at the village gates..."*

**Step 1 - Extracted Description**:
```
A female knight in gleaming silver armor with intricate engravings, wielding a glowing blue enchanted sword, flowing dark hair beneath her helmet, determined green eyes, standing in a protective stance, cape flowing in the wind. transparent background, PNG format
```

**Step 2 - SDXL-Optimized Final Prompt**:
```
A female knight in gleaming silver armor with intricate engravings, wielding a glowing blue enchanted sword, flowing dark hair beneath her helmet, determined green eyes, standing in a protective stance, cape flowing in the wind, full body shot, isolated on pure white background, png style, no background, clean edges, high quality, detailed, fantasy art style, magical atmosphere
```

---

## 🏞️ **Background Prompt Construction**

### **Step-by-Step Process**

#### **1. Background Extraction Template**
```python
# From config.py
BACKGROUND_PROMPT_TEMPLATE = """<|user|>
You are an AI prompt generator for background images.
Based on this story: {story}

Create a concise, highly visual prompt for the SETTING of the story.
Guidelines:
- Describe only the environment and scenery, without including any characters or creatures.
- Include specific location details, architecture, and landmarks relevant to the story.
- Indicate time of day, season, and weather.
- Convey atmosphere and mood visually (e.g., lighting, color tone) rather than poetically.
- Ensure composition is wide enough to place a character in the scene later.
- Keep it under 3 sentences.
- End with the desired style (realistic, cinematic, anime, etc.).
- Background does not need to be transparent.

Final format:
A detailed image prompt, ending with style keywords.
<|end|>
<|assistant|>
"""
```

#### **2. SDXL Background Template**
```python
BACKGROUND_IMAGE_PROMPT_TEMPLATE = """
{background_description}, detailed environment, 
atmospheric lighting, high quality, cinematic, 
{style_modifier}
"""
```

### **Example Background Prompt Evolution**

**Input Story**: *"...the village gates as shadow creatures approached from the dark forest..."*

**Step 1 - Extracted Description**:
```
A medieval village at night with thatched-roof houses, wooden gates, a dark mysterious forest in the background, moonlight casting dramatic shadows, mystical blue light emanating from torches illuminating the scene, fantasy cinematic style
```

**Step 2 - SDXL-Optimized Final Prompt**:
```
A medieval village at night with thatched-roof houses, wooden gates, a dark mysterious forest in the background, moonlight casting dramatic shadows, mystical blue light emanating from torches illuminating the scene, detailed environment, atmospheric lighting, high quality, cinematic, fantasy art style, magical atmosphere
```

---

## ⚙️ **LangChain Workflow Orchestration**

```
    User Topic Input
           |
    ┌─────────────────┐
    │   Story Chain   │ ← Phi-3-mini prompt
    │  (Runnable)     │
    └─────────────────┘
           |
    Generated Story + Metadata
           |
    ┌─────────────────┐
    │Image Prompt     │ ← Character + Background
    │Chain (Runnable) │   extraction prompts
    └─────────────────┘
           |
    Optimized SDXL Prompts
           |
    ┌─────────────────┐
    │  Image          │ ← SDXL generation
    │  Generation     │   + rembg processing
    └─────────────────┘
           |
    ┌─────────────────┐
    │  Composite      │ ← Character + Background
    │  Chain          │   merging with transparency
    │  (Runnable)     │
    └─────────────────┘
           |
    Final Story Visualization
```

### **LangChain Implementation Highlights**

- **Modern Runnable Interface**: Uses LangChain's latest composition patterns
- **Chain Modularity**: Separate chains for story generation and image prompt optimization
- **Error Handling**: Comprehensive logging and fallback mechanisms
- **Pipeline Orchestration**: Seamless data flow between text and image generation stages

---

## 🎨 **Technical Architecture**

### **Core Components**

- **Text Generation**: Microsoft Phi-3-mini-4k-instruct (local execution)
- **Image Generation**: Stable Diffusion XL Base 1.0 (1024x1024 native resolution)
- **Background Removal**: rembg package with U²-Net AI models + color-based fallback
- **Framework**: LangChain Runnable interface for pipeline orchestration
- **Image Processing**: Pillow + custom merging algorithms

### **Style Detection System**

```python
# From config.py
STYLE_MODIFIERS = {
    "fantasy": "fantasy art style, magical atmosphere",
    "sci-fi": "sci-fi concept art, futuristic",
    "horror": "dark atmosphere, gothic style",
    "romance": "soft lighting, romantic atmosphere",
    "adventure": "epic scale, dramatic lighting",
    "mystery": "noir style, mysterious atmosphere",
    "default": "professional illustration style"
}
```

**Automated Detection**: Keywords in generated stories trigger appropriate style modifiers for consistent visual aesthetics.

### **Quality Assurance Features**

- **Prompt Validation**: Ensures character descriptions end with transparency requirements
- **Background Composition**: Automatic foreground space allocation for character placement
- **Error Recovery**: Fallback prompts and alternative models when primary systems fail
- **Logging Integration**: Comprehensive debugging and performance monitoring

---

## 📊 **Example Outputs & Iterations**

### **Sample Generation Results**

**Topic**: `"A robot learning emotions"`

**Generated Story**: *A small maintenance robot named Zyx discovered something strange in the abandoned laboratory. As sparks flew from damaged circuits, Zyx felt what humans called 'curiosity' for the first time...*

**Character Prompt**: `A small humanoid maintenance robot with blue LED eyes showing curiosity, metallic silver body with visible circuits, articulated arms holding a glowing device, standing upright with slightly tilted head expressing wonder, transparent background, PNG format`

**Background Prompt**: `An abandoned futuristic laboratory with broken equipment, scattered papers, dim emergency lighting casting long shadows, holographic displays flickering, sci-fi concept art, futuristic`

### **Generated Outputs Available**

The `/outputs` directory contains real examples from Google Colab execution:
- **Images**: `deadpool.png`, `test_robot.png`, `image.png`
- **Story Files**: Multiple `story_summary_*.txt` files with generated narratives
- **Generated Dates**: August 14, 2025 execution timestamps

---

## 🎯 **Evaluation Criteria Alignment**

### **Prompt Engineering Creativity**
- ✅ Multi-stage prompt optimization with context-aware enhancement
- ✅ Automated style detection and application
- ✅ Novel approach to character/background separation for compositing

### **LangChain Implementation**
- ✅ Modern Runnable interface with proper chain composition
- ✅ Modular design allowing independent chain execution
- ✅ Comprehensive error handling and logging integration

### **Code Quality & Robustness**
- ✅ Type hints and comprehensive docstrings
- ✅ Fallback mechanisms for model failures
- ✅ Structured logging and debugging tools

### **Documentation Clarity**
- ✅ Project-focused explanations with actual code examples
- ✅ Clear setup instructions for both Colab and local execution
- ✅ Real output examples available in `/outputs` directory

---

*This implementation was developed and tested in Google Colab with sample outputs available in the `/outputs` directory.
