storysmith-ai/
│
├── langchain_app/                  # All LangChain orchestration lives here for now
│   ├── __init__.py
│   ├── chains/                     # All chain definitions
│   │   ├── __init__.py
│   │   ├── story_chain.py           # Generates story, character, background
│   │   └── image_prompt_chain.py    # Converts descriptions → image prompts
│   │
│   ├── utils/                       # Helper functions
│   │   ├── __init__.py
│   │   ├── image_merge.py           # PIL/OpenCV merging
│   │   └── error_handler.py         # Custom error logging
│   │
│   ├── templates/                   # Will later feed Django
│   │   └── output_template.html
│   │
│   ├── config.py                    # All constants, model paths, env vars
│   └── main.py                      # Entry point for running LangChain app standalone
│
├── django_app/                      # Placeholder for Django integration
│    ├── db.sqlite3
│    ├── main/
│    │   ├── admin.py
│    │   ├── apps.py
│    │   ├── forms.py
│    │   ├── __init__.py
│    │   ├── migrations
│    │   │   └── __init__.py
│    │   ├── models.py
│    │   ├── templates
│    │   │   └── main
│    │   │       ├── base.html
│    │   │       ├── input_form.html
│    │   │       └── result.html
│    │   ├── tests.py
│    │   ├── urls.py
│    │   └── views.py
│    ├── manage.py
│    ├── media/
│    ├── requirements.txt
│    ├── static
│    ├── storysmith/
│    │   ├── asgi.py
│    │   ├── __init__.py
│    │   ├── settings.py
│    │   ├── urls.py
│    │   └── wsgi.py
│    └── storysmith.log
│
├── colab/                           # Colab notebooks for heavy inference
│   └── image_gen_colab.ipynb        # Stable Diffusion/HF image generation
│
├── .gitignore
├── requirements.txt
└── README.md
