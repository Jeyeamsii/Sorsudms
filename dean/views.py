from django.shortcuts import render,redirect, get_object_or_404
from .models import CustomUser,Department,Role,Program
from .forms import CustomUserCreationForm,CustomUserEditForm
from django.template.loader import render_to_string
from django.http  import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required #to enforce constraint to views
from django.contrib import messages  #built-in system that allows you to display one-time notifications to your users. It's a way to provide feedback to users after they've performed a certain action, such as submitting a form, deleting an object, or logging in.
from django.db.models import Q  #for complex queries, used in search functionality
from django.contrib.auth import get_user_model  #returns the user model that is currently active in the project
from django.core.mail import send_mail,EmailMultiAlternatives #Django's email handling module for sending emails
from django.utils.http import urlsafe_base64_encode ,urlsafe_base64_decode #function from django's utilities, useful for encoding/decoding data in a way that is safe to include in URLs
from django.utils.encoding import force_bytes, force_str  #essential for converting various data types into a bytes-like object, which is particularly useful when working with functions that require byte input, such as urlsafe_base64_encode.
from .tokens import account_activation_token  #importing the token that is created at tokens.py
from django.utils.html import strip_tags
from faculty.models import Document
from .decorators import role_required






# Create your views here
@login_required  #to restrict access to the view. It requires authenticated user
@role_required('Dean')
def home_page(request):
  return render(request, 'dean/homepage.html')



@login_required
@role_required('Dean')
def userManagement(request):
  # exclude users with specified roles and staff users
  exclude_roles = [3,4]

  # get search query from GET parameters
  query = request.GET.get('search', '')
  if query:
     # filter users based on search query
     users = CustomUser.objects.filter(Q(first_name__icontains=query)|Q(username__icontains=query)|Q(program__name__icontains=query)|Q(first_name__icontains=query)|Q(last_name__icontains=query)|Q(program__name__icontains=query) ).exclude(role__in=exclude_roles).exclude(is_staff=True).exclude(is_archived=True)   #this search query will filter user with the first_name/username provided in the seach field
  else:
     users = CustomUser.objects.exclude(role__in=exclude_roles).exclude(is_staff=True).exclude(is_archived=True) # this filters the list of users that will be rendered in the usermanagement page, so this excludes the Dean and QAO with an id of 3 and 4 respectively

  dean= request.user
  department = dean.department
  # Initialize the form with the current dean
  form = CustomUserCreationForm(dean=dean)
  return render(request, 'dean/UserManagement.html',{'users':users, 'form':form, 'department':department, 'query':query})



User = get_user_model() # to retreive the user model that is currently active in the project


# view for creating faculty users
@login_required
@role_required('Dean')
def create_user(request):
  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST, dean=request.user)
    if form.is_valid():
         user = form.save(commit=False)
         user.is_active = False     #deactivate account until email verification

          #save the user
         user.save()
         #form.save()



         #send verification email
         mail_subject = 'Activate your account.'
         message = render_to_string('dean/account_activation_email.html', {
         'user': user,
         'domain': request.META['HTTP_HOST'],
         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
         'token': account_activation_token.make_token(user),
      })
         plain_message = strip_tags(message)
         email = EmailMultiAlternatives(mail_subject, plain_message,'arikashikarimikutarimo@gmail.com',[user.email])
         email.attach_alternative(message, "text/html")
         email.send()


         messages.success(request, 'User succesfully created!') #show alert after a new user is created
         return JsonResponse({"success": True})


    else:
      # #is used to render a Django template into a string, which is then returned as part of a JSON response. This is particularly useful in AJAX requests where you want to update part of a web page without a full page reload.
      html_form = render_to_string('dean/create_user_form.html',{'form':form}, request=request)
      return JsonResponse({'success':False, 'html_form':html_form})

  else:
       dean= request.user
       form = CustomUserCreationForm(dean=dean)
       return render(request,'dean/create_user_form.html', {'form':form})








#a view for handling the activation link in the verification email, this will verify the token and activate the user account
def activate(request, uidb64, token):
   try:
      uid = force_str(urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=uid)
   except(TypeError, ValueError, OverflowError, User.DoesNotExist):
      user = None

   if user is not None and account_activation_token.check_token(user, token):
      user.is_active = True
      user.save()
      return render(request, 'dean/activation_success.html')
   else:
      return render(request, 'dean/activation_invalid.html')






#view for editing user info
@login_required
@role_required('Dean')
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=user, dean=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "User's information successfully edited!") #show alert after an existing user is edited
            return JsonResponse({'success': True})
        else:
            form_html = render_to_string('dean/edit_user_form.html', {'form': form}, request=request)
            return JsonResponse({'success': False, 'form_html': form_html})
    else:
        form = CustomUserEditForm(instance=user, dean=request.user)
    return render(request, 'dean/edit_user_form.html', {'form': form, 'user':user})



# view for displaying approved documents
@role_required('Dean')
def department_files_view(request):
   dean = request.user

   query = request.GET.get('search','') # get the search term
   if query:
      documents = Document.objects.filter(department=dean.department).filter(status='Approved').filter(Q(document_type__icontains=query)| Q(submitted_by__username__icontains=query)| Q(program__name__icontains=query)| Q(document_name__icontains=query))

   else:
      documents = Document.objects.filter(department=dean.department).filter(status='Approved')


   return render(request,'dean/files.html',{'documents':documents, 'query':query})





# view in setting the is_archive attribute to True
@role_required('Dean')
def archive_user(request, user_id):
   user = get_object_or_404(CustomUser, id=user_id)

   user.is_archived = True
   user.save()

   messages.success(request, 'User has been successfully archived.')
   return redirect('userManagement')


# view in displaying the archived user in the template
@role_required('Dean')
def list_of_archived_user(request):
   dean = request.user

   query = request.GET.get('search', '')
   if query:
       archived_users = CustomUser.objects.filter(is_archived=True).filter(department=dean.department).filter(Q(username__icontains=query)| Q(first_name__icontains=query)| Q(last_name__icontains=query))
   else:
       archived_users = CustomUser.objects.filter(is_archived=True).filter(department=dean.department)

   return render(request, 'dean/archived_users.html',{'archived_users':archived_users})



@role_required('Dean')
def delete_user(request, user_id):
   user = get_object_or_404(CustomUser, id=user_id)
   if user.is_archived:
      user.delete()

      messages.success(request, f'Archived user account "{user.username}" has been permanently deleted.')
      return redirect('list-of-archived-users')


@role_required('Dean')
def restore_user(request, user_id):
   user = get_object_or_404(CustomUser, id=user_id)
   if user.is_archived:
      user.is_archived = False
      user.is_active = True
      user.save()

      messages.success(request, f'Archived User Account "{user.username}" has been successfully restored!')
      return redirect('list-of-archived-users')





def trash_bin(request):
    trashed_documents = Document.trash.all()

    query = request.GET.get('search','') # get the search term
    if query:
       trashed_documents = Document.trash.filter(Q(document_name__icontains=query))

    return render(request, 'dean/trash_bin.html', {'documents': trashed_documents})


def soft_delete_document(request, document_id):
  document = get_object_or_404(Document, id=document_id)
  document.soft_delete()  # Call the soft delete method
  return redirect('department-files')  # Redirect to the documents list page


def restore_document(request, document_id):
    document = get_object_or_404(Document.trash, id=document_id)
    document.restore()
    return redirect('trash_bins')


def delete_permanently(request, document_id):
    document = get_object_or_404(Document.trash, id=document_id)
    document.delete_permanently()
    return redirect('trash_bins')


from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
   queryset = CustomUser.objects.all()
   serializer_class = CustomUserSerializer

