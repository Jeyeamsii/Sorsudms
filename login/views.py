from django.shortcuts import render, redirect
from django.urls import reverse   #converts URL names back into URL strings
from django.contrib.auth import login,authenticate,logout  # important in managing user authentication, making it easy to manage login,logout and user authentication
from .forms import LoginForm
from django.contrib import messages

# Create your views here.

#a view for login and authenticates the user
def login_view(request):
  if request.method == "POST":
    form = LoginForm(request,data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username,password=password)

      if user is not None:
        login(request, user)
        #check user role and redirect them to their dashboard
        messages.success(request, 'Login successful!')  #display an alert for successful login
        if user.role.name == 'Dean':
          next_page = reverse('dean-homepage')
        elif user.role.name == "Faculty":
          next_page = reverse('faculty-homepage')
        elif user.role.name == "Program Chair":
          next_page = reverse('pc-homepage')
        elif user.role.name == "Quality Assurance Officer":
          next_page = reverse('qao-homepage')

      return render(request, 'login/Login.html', {'form':form,'next':next_page, 'show_modal':True})


  else:
         form = LoginForm()#This ensures an empty form on GET request

  return render(request, 'login/Login.html', {'form':form, 'show_modal':False})


# logout view
def log_out(request):
  logout(request)
  return redirect(reverse('login'))

