from django import forms
from .models import SubmissionBin
from .validators import validate_academic_year

class SubmissionBinForm(forms.ModelForm):
  #creating a  form based from the submision bin model
  
  academic_year = forms.CharField(max_length=9,widget=forms.TextInput(attrs={'placeholder': 'YYYY-YYYY', 'class': 'form-control'}), validators=[validate_academic_year], required=True) 
  semester = forms.ChoiceField(choices=SubmissionBin.SEMESTER_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), required=True)
  category = forms.ChoiceField(choices=SubmissionBin.CATEGORY, widget=forms.Select(attrs={'class': 'form-select'}), required=True)

  class Meta:
    model = SubmissionBin
    fields = ['category','deadline','semester','academic_year','department','program']
    # add widgets dictionary to specify custom widgets for each field. each key corresponds to a field name, and the value is an instance of a widget class(like TextInput etc.)
    widgets = {
      
      'deadline': forms.DateTimeInput(attrs={
        'class': 'form-control',
        'placeholder': 'YYYY-MM-DD HH:MM',
        'type': 'datetime-local',  # Use datetime local for better UX
        'required':'required' # make the field required
      }),
    }
  


class EditSubmissionBinForm(forms.ModelForm):
  #creating a  form based from the submision bin model
  
  academic_year = forms.CharField(max_length=9,widget=forms.TextInput(attrs={'placeholder': 'YYYY-YYYY', 'class': 'form-control'}), validators=[validate_academic_year], required=True) 
  semester = forms.ChoiceField(choices=SubmissionBin.SEMESTER_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}), required=True)
  category = forms.ChoiceField(choices=SubmissionBin.CATEGORY, widget=forms.Select(attrs={'class': 'form-select'}), required=True)

  class Meta:
    model = SubmissionBin
    fields = ['category','deadline','semester', 'academic_year', 'program', 'department']
    # add widgets dictionary to specify custom widgets for each field. each key corresponds to a field name, and the value is an instance of a widget class(like TextInput etc.)
    widgets = {
      
      'deadline': forms.DateTimeInput(attrs={
        'class': 'form-control',
        'placeholder': 'YYYY-MM-DD HH:MM',
        'type': 'datetime-local',  # Use datetime local for better UX
        'required':'required' # make the field required
      }),
    }
  

