from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('name', 'description', 'file')
        widgets = {
            "name" : forms.TextInput(attrs={'class': 'h-12 px-3 w-full border-blue-400 border-2 rounded focus:outline-none focus:border-blue-600'}),
            "description" : forms.Textarea(attrs={'class': 'h-24 py-1 px-3 w-full border-2 border-blue-400 rounded focus:outline-none focus:border-blue-600 resize-none'}),
            "file" : forms.FileInput(attrs={'class': 'h-full w-full opacity-0'})
        }