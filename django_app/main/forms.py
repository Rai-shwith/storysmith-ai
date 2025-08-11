"""
Forms for StorySmith AI main app.
Handles user input for story generation including text prompts and audio uploads.
"""

from django import forms


class StoryInputForm(forms.Form):
    """
    Form for capturing user input for story generation.
    Includes text prompt (required) and optional audio file upload.
    """
    
    # Text prompt field - required, max 300 characters
    text_prompt = forms.CharField(
        max_length=300,
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your story prompt here... (max 300 characters)',
            'rows': 4,
            'maxlength': 300,
            'id': 'text_prompt'
        }),
        label='Story Prompt',
        help_text='Describe the story you want to generate (required, max 300 characters)'
    )
    
    # Audio file upload - optional
    audio_file = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'audio/*',
            'id': 'audio_file'
        }),
        label='Audio File (Optional)',
        help_text='Upload an audio file or use the microphone to record'
    )
    
    def clean_text_prompt(self):
        """
        Validate text prompt length and content.
        """
        text_prompt = self.cleaned_data.get('text_prompt')
        
        if text_prompt:
            # Remove extra whitespace
            text_prompt = text_prompt.strip()
            
            # Check if text is not empty after stripping
            if not text_prompt:
                raise forms.ValidationError('Text prompt cannot be empty.')
            
            # Check length
            if len(text_prompt) > 300:
                raise forms.ValidationError('Text prompt must be 300 characters or less.')
        
        return text_prompt
    
    def clean_audio_file(self):
        """
        Validate audio file upload.
        """
        audio_file = self.cleaned_data.get('audio_file')
        
        if audio_file:
            # Check file size (max 10MB)
            if audio_file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('Audio file must be smaller than 10MB.')
            
            # Check if it's an audio file (basic check)
            if not audio_file.content_type.startswith('audio/'):
                raise forms.ValidationError('Please upload a valid audio file.')
        
        return audio_file
