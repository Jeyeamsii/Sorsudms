from django import forms
from django.contrib.auth.forms import AuthenticationForm  #Django's built-in form used for handling user authentication, it includes built-in validation for checking credentials and ensuring the user is active, it also manages error messages if the authentication fails


class LoginForm(AuthenticationForm):
  username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-lg bg-light fs-6','placeholder':'Enter Username'}))
  # use widget attribute to customize the HTML attributes of the form fields

  password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control form-control-lg bg-light fs-6','placeholder':'Enter Password'}))
