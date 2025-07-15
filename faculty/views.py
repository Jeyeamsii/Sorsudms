from django.shortcuts import render, get_object_or_404, redirect #a utility function provided by Django that simplifies the process of retrieving an object from the database while handling the case where the object does not exist. It is commonly used in Django views to fetch a single object based on a given query, and it automatically raises a 404 Not Found error if the object is not found. This is particularly useful for improving user experience by providing a clear response when a requested resource is not available.
from django.contrib.auth.decorators import login_required, user_passes_test
from dean.models import CustomUser
from pc.models import SubmissionBin, Notification
from .models import Document
from pc.views import notify_users
from .forms import DocumentForm
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from pc.models import Notification
import requests
import os
from dean.decorators import role_required
from django.db.models import Q
# Create your views here.


@role_required('Faculty')
def home(request):
  return render(request,'faculty/home.html')




#@role_required('Faculty')
#def files(request):
 # user = CustomUser.objects.get(username=
#  request.user)

 # approved_documents = Document.objects.filter(submitted_by = user.id).filter(status="Approved").order_by('-date_submitted')

 # declined_documents = Document.objects.filter(submitted_by = user.id).filter(status="Declined").order_by('-date_submitted')

 # pending_documents = Document.objects.filter(submitted_by = user.id).filter(status="Pending").order_by('-date_submitted')



#  return render(request,'faculty/Files.html',{'approved_documents':approved_documents, 'declined_documents':declined_documents, 'pending_documents':pending_documents})




@role_required('Faculty')
def submissionBinList(request):
  #get user's department and program
  faculty_user = request.user
  department = faculty_user.department
  program = faculty_user.program

  #filter submission bins by user's department and program
  submission_bins = SubmissionBin.objects.filter(department=department, program=program).order_by('-date_created')

  query = request.GET.get('search', '')
  # this filters the documents by search
  if query:
    submission_bins = submission_bins.filter(Q(academic_year__icontains=query)| Q(category__icontains=query))


  return render(request, 'faculty/submission_bin_list.html',{'submission_bins':submission_bins})





@role_required('Faculty')
def submit_document(request, submission_bin_id):
  submission_bin = get_object_or_404(SubmissionBin, id=submission_bin_id)
  if request.method == 'POST':
    form = DocumentForm(request.POST,request.FILES)
    if form.is_valid():
      document = form.save(commit=False)
      document.submission_bin = submission_bin
      document.submitted_by = request.user
      document.department = request.user.department
      document.program = request.user.program
      document.document_type = submission_bin.category
      document.status = 'Pending'
      document.save()



      #notify pc whenever new document was submitted
      notify_users(f"New document was submitted by '{request.user}'",receipient = submission_bin.created_by )
      messages.success(request, 'Document was successfully submitted!')
      return JsonResponse({"success": True})

    else:
      html_form = render_to_string('faculty/submit_document.html',{'form':form}, request=request)
      return JsonResponse({'success':False, 'html_form':html_form})

  else:
    form = DocumentForm()
    return render(request, 'faculty/submit_document.html',{'form':form, 'submission_bin':submission_bin})







#def document_viewer(request, document_id):

  #fetch the document object
 # document = get_object_or_404(Document, id=document_id)

  #generate the full URL for the file
#  document_url = request.build_absolute_uri(document.file.url)

  #pass the url to the template
#  return render(request, 'faculty/document_viewer.html', {'document_url':document_url})





#function for creating a notification record that will be saved in the database
def notify_users(message,receipient):
  Notification.objects.create(message=message, receipient=receipient)




# view for viewing faculty notifications
@role_required('Faculty')
def faculty_notification_list(request):
  notifications = Notification.objects.filter(receipient=request.user).order_by('-date_created')
  return render(request, 'faculty/notifications.html', {'notifications':notifications})



# view for changing the read attribute of notification to true
def mark_as_read(request, notification_id):
  notification = get_object_or_404(Notification, id=notification_id)
  notification.read = True
  notification.save()
  return redirect('faculty-notifications')



#view for counting unread notification
def unread_notification_count(request):
  unread_count = Notification.objects.filter(receipient=request.user).filter(read=False).count()
  return JsonResponse({'unread_count':unread_count})




# view that handles viewing documents
def document_viewer(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    doc_url = request.build_absolute_uri(document.file.url)
    return render(request, 'faculty/document_viewer.html', {'doc_url': doc_url})




def trash_bin(request):


    trashed_documents = Document.trash.all()

    query = request.GET.get('search', '')
    # this filters the documents by search
    if query:
      trashed_documents = trashed_documents.filter(Q(document_name__icontains=query))


    return render(request, 'faculty/trash_bin.html', {'documents': trashed_documents})




def soft_delete_document(request, document_id):
  document = get_object_or_404(Document, id=document_id)
  document.soft_delete()  # Call the soft delete method
  return redirect('faculty-files')  # Redirect to the documents list page


def restore_document(request, document_id):
    document = get_object_or_404(Document.trash, id=document_id)
    document.restore()
    return redirect('trash_bin')


def delete_permanently(request, document_id):
    document = get_object_or_404(Document.trash, id=document_id)
    document.delete_permanently()
    return redirect('trash_bin')






def files_view(request):
    user = request.user
    tab = request.GET.get('tab', 'pending')  # Get the current tab from the query params
    query = request.GET.get('search', '')  # Get the search query

    # Filter documents based on the tab
    if tab == 'pending':
        documents = Document.objects.filter(submitted_by=user, status="Pending")
    elif tab == 'approved':
        documents = Document.objects.filter(submitted_by=user, status="Approved")
    elif tab == 'declined':
        documents = Document.objects.filter(submitted_by=user, status="Declined")


    # Apply search filter if a query is present
    if query:
        documents = documents.filter(
            Q(document_type__icontains=query) |
            Q(submitted_by__username__icontains=query) |
            Q(program__name__icontains=query) |
            Q(document_name__icontains=query)
        )

    return render(request, 'faculty/Files.html', {
        'documents': documents,
        'tab': tab,
        'query': query,
    })
