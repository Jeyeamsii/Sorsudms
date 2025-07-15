from django import forms
from .models import QAOFile

class QAOFileUploadForm(forms.ModelForm):
  class Meta:
    model = QAOFile
    fields = ['document_name', 'file']


