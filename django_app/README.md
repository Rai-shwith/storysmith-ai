# StorySmith AI - Django Web Interface

A Django web application that provides a user-friendly interface for AI-powered story generation. This app serves as the web frontend that integrates with the LangChain-powered backend for creative storytelling.

## 🎯 **Overview**

The Django app provides a clean web interface where users can:
- Enter text prompts for story generation
- Upload audio files for voice-based story prompts
- View generated stories with character and background descriptions
- Experience real-time story creation through a responsive web interface

## 📁 **Project Structure**

```
django_app/
├── manage.py                    # Django management script
├── db.sqlite3                   # SQLite database (minimal usage)
├── requirements.txt             # Django dependencies
├── storysmith.log              # Application logs
├── main/                       # Main Django application
│   ├── __init__.py
│   ├── admin.py                # Admin configuration
│   ├── apps.py                 # App configuration
│   ├── forms.py                # Form definitions
│   ├── models.py               # Database models
│   ├── tests.py                # Test cases
│   ├── urls.py                 # URL routing
│   ├── views.py                # View logic
│   ├── migrations/             # Database migrations
│   └── templates/main/         # HTML templates
│       ├── base.html           # Base template
│       ├── input_form.html     # Story input form
│       └── result.html         # Story results display
├── media/
│   └── audio_uploads/          # Uploaded audio files
├── static/                     # Static files (CSS, JS, images)
└── storysmith/                 # Django project settings
    ├── __init__.py
    ├── asgi.py                 # ASGI configuration
    ├── settings.py             # Project settings
    ├── urls.py                 # Main URL configuration
    └── wsgi.py                 # WSGI configuration
```

## 🚀 **Quick Start**

### 1. **Prerequisites**
- Python 3.8+
- Django 4.2+
- Working LangChain app (from `../langchain_app/`)

### 2. **Installation**

```bash
# Navigate to Django app directory
cd django_app

# Install Django dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create superuser (optional, for admin access)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### 3. **Access the Application**

- **Web Interface**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/ (if superuser created)

## 🔗 **LangChain Integration**

### **How Django Connects to LangChain**

The Django app integrates with the LangChain backend through direct Python imports:

```python
# In views.py
import sys
import os

# Add LangChain app to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'langchain_app'))

# Import LangChain components
from chains.composite_chain import create_story_visualization_chain
from utils.error_handler import log_error, StorySmithError
```

### **Using Chains in Django Views**

```python
def generate_story_view(request):
    """
    Main view for story generation using LangChain backend.
    """
    if request.method == 'POST':
        form = StoryInputForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Get user input
                topic = form.cleaned_data['text_prompt']
                
                # Create LangChain chain
                chain = create_story_visualization_chain()
                
                # Execute story generation
                result = chain.invoke({"topic": topic})
                
                # Return results to template
                return render(request, 'main/result.html', {
                    'result': result,
                    'topic': topic,
                    'success': True
                })
                
            except StorySmithError as e:
                # Handle LangChain-specific errors
                return render(request, 'main/input_form.html', {
                    'form': form,
                    'error': f"Story generation failed: {e}",
                    'error_type': 'langchain'
                })
                
z            except Exception as e:
                # Handle general errors
                log_error(f"Unexpected error in Django view: {e}")
                return render(request, 'main/input_form.html', {
                    'form': form,
                    'error': "An unexpected error occurred. Please try again.",
                    'error_type': 'general'
                })
    else:
        form = StoryInputForm()
    
    return render(request, 'main/input_form.html', {'form': form})
```

### **Configuration Sharing**

Both Django and LangChain apps share the same configuration:

```python
# Configuration is shared through:
# 1. Environment variables (.env files)
# 2. Python path manipulation
# 3. Direct imports

# Example in Django settings.py
import os
from dotenv import load_dotenv

# Load environment variables (same as LangChain app)
load_dotenv(os.path.join(BASE_DIR, '..', 'langchain_app', '.env'))

# Access shared configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN')
```

### **Error Handling for LangChain Operations**

```python
from utils.error_handler import StorySmithError, log_error

def handle_langchain_errors(request, form):
    """
    Centralized error handling for LangChain operations.
    """
    try:
        # LangChain operation
        result = chain.invoke({"topic": topic})
        return result
        
    except StorySmithError as e:
        # Log the error
        log_error(f"LangChain error: {e}")
        
        # User-friendly error messages
        error_messages = {
            'API_ERROR': 'Service temporarily unavailable. Please try again.',
            'VALIDATION_ERROR': 'Invalid input. Please check your prompt.',
            'GENERATION_ERROR': 'Story generation failed. Please try a different prompt.',
        }
        
        error_type = getattr(e, 'error_type', 'GENERAL')
        user_message = error_messages.get(error_type, str(e))
        
        return render(request, 'main/input_form.html', {
            'form': form,
            'error': user_message,
            'show_retry': True
        })
```

## 📝 **Web Forms & User Input**

### **Story Input Form**

The main form (`StoryInputForm`) handles:

```python
class StoryInputForm(forms.Form):
    # Text prompt (required, max 300 characters)
    text_prompt = forms.CharField(
        max_length=300,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your story prompt here...',
            'rows': 4,
            'maxlength': 300
        })
    )
    
    # Audio file upload (optional, max 10MB)
    audio_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'accept': 'audio/*'
        })
    )
```

### **Form Validation**

- **Text Prompt**: Required, max 300 characters, whitespace validation
- **Audio File**: Optional, max 10MB, audio format validation
- **Security**: File type validation, size limits, XSS protection

### **User Experience Features**

- Character count display for text prompts
- Audio file preview and validation
- Real-time form validation
- Progress indicators during story generation
- Error messages with retry options

## 🎨 **Templates & UI**

### **Template Structure**

```html
<!-- base.html - Common layout -->
<!DOCTYPE html>
<html>
<head>
    <title>StorySmith AI</title>
    <!-- Bootstrap, custom CSS -->
</head>
<body>
    <nav><!-- Navigation --></nav>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer><!-- Footer --></footer>
</body>
</html>

<!-- input_form.html - Story input form -->
{% extends 'main/base.html' %}
{% block content %}
    <form method="post" enctype="multipart/form-data">
        {{ form.as_p }}
        <button type="submit">Generate Story</button>
    </form>
{% endblock %}

<!-- result.html - Story results display -->
{% extends 'main/base.html' %}
{% block content %}
    <div class="story-result">
        <h2>Generated Story</h2>
        <div class="story-content">{{ result.story }}</div>
        <div class="character-description">{{ result.character_description }}</div>
        <div class="background-description">{{ result.background_description }}</div>
    </div>
{% endblock %}
```

### **Responsive Design**

- Bootstrap-based responsive layout
- Mobile-friendly form inputs
- Touch-friendly audio upload interface
- Progressive enhancement for JavaScript features

## 🔧 **Development Workflow**

### **Local Development Setup**

```bash
# 1. Set up Django app
cd django_app
python manage.py migrate
python manage.py runserver

# 2. Ensure LangChain app is configured
cd ../langchain_app
# Make sure .env file has required API keys

# 3. Test integration
# Visit http://127.0.0.1:8000/ and test story generation
```

### **Environment Variables**

Required environment variables (shared with LangChain app):

```bash
# In langchain_app/.env (shared configuration)
GOOGLE_API_KEY=your_google_api_key_here
HUGGINGFACE_API_TOKEN=your_huggingface_token_here
OUTPUT_DIR=./outputs
TEMP_DIR=./temp
LOG_FILE=storysmith.log
```

### **Testing the Integration**

```bash
# Test Django app
python manage.py test

# Test LangChain integration manually
python manage.py shell
>>> from main.views import generate_story_view
>>> # Test view logic
```

## 🚨 **Error Handling & Debugging**

### **Common Issues**

1. **LangChain Import Errors**
   ```python
   # Fix: Ensure Python path includes langchain_app
   sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'langchain_app'))
   ```

2. **API Key Errors**
   ```python
   # Fix: Check environment variable loading
   from dotenv import load_dotenv
   load_dotenv('../langchain_app/.env')
   ```

3. **File Upload Issues**
   ```python
   # Fix: Check media settings in settings.py
   MEDIA_URL = '/media/'
   MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
   ```

### **Logging & Monitoring**

```python
# Django logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'storysmith.log',
        },
    },
    'root': {
        'handlers': ['file'],
    },
}
```

## 🔄 **Data Flow**

```
User Input (Web Form)
    ↓
Django Form Validation
    ↓
Django View Processing
    ↓
LangChain Chain Invocation
    ↓
Story Generation (Google Gemini API)
    ↓
Image Prompt Generation
    ↓
Result Processing
    ↓
Template Rendering
    ↓
HTML Response to User
```

## 🛡️ **Security Considerations**

- **CSRF Protection**: Django CSRF tokens on all forms
- **File Upload Security**: File type and size validation
- **Input Sanitization**: Form validation and cleaning
- **API Key Security**: Environment variables, never in code
- **Error Handling**: No sensitive data in error messages

## 📚 **Next Steps**

For more detailed information about the AI backend:
- See `../langchain_app/README.md` for LangChain implementation details
- Check `../langchain_app/` for configuration options
- Review error handling patterns in `utils/error_handler.py`

This Django app provides a robust web interface for the StorySmith AI system, focusing on user experience while seamlessly integrating with the powerful LangChain backend for story generation.
