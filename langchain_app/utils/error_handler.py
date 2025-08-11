# storysmith-ai/langchain_app/utils/error_handler.py

import traceback

def log_error(e):
    print("\n[ERROR]", str(e))
    print(traceback.format_exc())
