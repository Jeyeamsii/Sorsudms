from django import forms
from django.contrib.auth.forms import UserCreationForm # built-in form to handle user creation tasks, especifically for registering new users
from .validators import validate_birthday,validate_letters_only   #importing the validators that we created in validators.py
from django.core.exceptions import ValidationError
from .models import CustomUser,Department,Role,Program


# forms for creating users
class CustomUserCreationForm(UserCreationForm):
  department = forms.ModelChoiceField(queryset=Department.objects.all(),disabled=True)

  role = forms.ModelChoiceField(queryset=Role.objects.all())

  address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control p-2', 'type':'text','placeholder': 'Enter your address'}), required=True)

  username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class':'form-control p-2', 'type':'text','placeholder': 'Enter username'}))

  email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control p-2', 'type':'email','placeholder': 'Enter Email address'}))

  first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control p-2', 'type':'text','placeholder': 'Enter firstname'}), validators=[validate_letters_only])

  middle_initial = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control w-50 p-2', 'type':'text','placeholder': 'M.I'}), max_length=1, validators=[validate_letters_only])

  last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control p-2', 'type':'text','placeholder': 'Enter lastname'}), validators=[validate_letters_only])

  program = forms.ModelChoiceField(queryset=Program.objects.all(),required=True,)


  birthday = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'p-2'}), required=True, validators=[validate_birthday])

  password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control p-2', 'placeholder': 'Enter a Password'}))

  password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control p-2', 'placeholder': 'Confirm Password'}))


  class Meta:
    model = CustomUser
    fields = ('username','first_name','last_name','email','department','role','address','password1','password2','program','middle_initial','birthday')


  def __init__(self,*args,**kwargs):
    self.dean = kwargs.pop('dean',None)
    super().__init__(*args,**kwargs)
    if self.dean:
      self.fields['department'].initial = self.dean.department
      self.fields['department'].queryset=Department.objects.filter(id=self.dean.department.id)  #Sets the initial value of the department field to the dean's department

     


      self.fields['role'].queryset = Role.objects.exclude(name='Quality Assurance Officer').exclude(name='Dean')

      self.fields['program'].queryset=Program.objects.filter(department=self.dean.department.id)#Filters the program field to only include programs within the dean's department

  
  def clean(self):
     cleaned_data = super().clean()
     programs = cleaned_data.get("program")
     role = cleaned_data.get('role')

     # custom form validation
     if role.name == 'Program Chair':
  
        if CustomUser.objects.filter(program=programs, role__name='Program Chair').exists():
            raise ValidationError(f"A Program Chair account already exists for the {programs.name} program.")
     
     return cleaned_data




  def save(self, commit=True):
      user = super().save(commit=False)
      if self.dean:
        user.department = self.dean.department # set the department to the dean's department

      if commit:
        user.save()
      return user







#form for editing user info
class CustomUserEditForm(forms.ModelForm):
  department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, disabled=True)
  
  address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control p-2', 'type':'text','placeholder': 'Enter your address'}), required=True)

  username = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'class':'form-control p-2', 'type':'text','placeholder': 'Enter username'}))

  email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control p-2', 'type':'email','placeholder': 'Enter Email address'}))

  first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control p-2', 'type':'text','placeholder': 'Enter firstname'}), validators=[validate_letters_only])

  middle_initial = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control w-50 p-2', 'type':'text','placeholder': 'M.I'}), max_length=1, validators=[validate_letters_only])

  last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control p-2', 'type':'text','placeholder': 'Enter lastname'}), validators=[validate_letters_only])

  role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True, disabled=True)

  program = forms.ModelChoiceField(queryset=Program.objects.all(),required=True)


  birthday = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class':'p-2'}), required=True, validators=[validate_birthday])



  class Meta:
    model = CustomUser
    fields =('username','first_name','last_name','email','department','role','address','program','middle_initial','birthday')


  def __init__(self, *args, **kwargs):
    self.dean = kwargs.pop('dean',None)
    super().__init__(*args,**kwargs)
    if self.dean:
      self.fields['program'].queryset=Program.objects.filter(department=self.dean.department.id)

   # if self.instance and self.instance.pk:  # Check if editing an existing user
     # if self.instance.role.name == 'Program Chair':  # Check the role of the user
         # self.fields.pop('program')  # Remove the program field if the user is a Program Chair


  def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username
