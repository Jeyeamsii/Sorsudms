from django import forms
from .models import Document
from django.core.exceptions import ValidationError
 
class DocumentForm(forms.ModelForm):
  class Meta:
    model = Document
    fields = ['file', 'document_name']
    # use widgets to customize the input fields
    widgets = {
      'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
      'document_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter name'})
    }
  # add validation in the form for extra validation layer
  def clean_file(self):
    file = self.cleaned_data.get('file')

    
    #check the file size
    max_size = 20 * 1024 * 1024  #20MB in bytes
    if file.size > max_size:
      raise ValidationError('File size cannot exceed 20MB.')
    
    return file