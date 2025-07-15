from django.shortcuts import render,redirect, get_object_or_404
from .forms import SubmissionBinForm, EditSubmissionBinForm
from dean.models import CustomUser,Program
from faculty.models import Document
from .models import Notification, SubmissionBin
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from dean.decorators import role_required
from django.db.models import Q
# Create your views here.




@role_required('Program Chair')
def homepage(request):
  return render(request, 'pc/homepage.html')




@role_required('Program Chair')
def submission(request):
  user_bins = SubmissionBin.objects.filter(created_by=request.user).order_by('-date_created') # get bins created by the user

  query = request.GET.get('search', '')
  # this filters the documents by search
  if query:
    user_bins = user_bins.filter(Q(academic_year__icontains=query)| Q(category__icontains=query))


  return render(request, 'pc/submission.html', {'user_bins':user_bins})




@role_required('Program Chair')
def create_submission_bin(request):
    if request.method == 'POST':
        form = SubmissionBinForm(request.POST)
        if form.is_valid():
            submission_bin = form.save(commit=False)
            submission_bin.created_by = request.user
            submission_bin.department = request.user.department
            submission_bin.program = request.user.program


            submission_bin.save()

            notify_users(f"New submission Bin for '{submission_bin.academic_year} - {submission_bin.semester}' was created", user_role_id=1,program=request.user.program)  #notify faculty users whenever a new submission bin was created
            messages.success(request, 'Submission Bin created successfully!')
            return JsonResponse({"success": True})

        else:
           print(f"Form errors: {form.errors}")
           html_form = render_to_string('pc/create_submission_bin.html',{'form':form}, request=request)
           return JsonResponse({'success':False, 'html_form':html_form})
    else:
       form = SubmissionBinForm()
       return render(request,'pc/create_submission_bin.html', {'form':form})




@role_required('Program Chair')
def edit_submission_bin(request,user_bin_id):
    bin = get_object_or_404(SubmissionBin, id=user_bin_id)

    if request.method == 'POST':
        form = EditSubmissionBinForm(request.POST, instance=bin)
        if form.is_valid():
            form.save()
            #notify_users(f"New submission Bin for '{submission_bin.academic_year} - {submission_bin.semester}' was created", user_role_id=1,program=request.user.program)  #notify faculty users whenever a new submission bin was created
            messages.success(request, 'Submission Bin was successfully edited!')
            return JsonResponse({"success": True})

        else:
           html_form = render_to_string('pc/edit_submission_bin.html',{'form':form, 'bin': bin}, request=request)
           return JsonResponse({'success':False, 'html_form':html_form})
    else:
       form = EditSubmissionBinForm(instance=bin)

    return render(request, 'pc/edit_submission_bin.html', {'form': form, 'bin':bin})




@role_required('Program Chair')
def confirm_delete_submission_bin(request,submission_bin_id):
   submission_bin = get_object_or_404(SubmissionBin, id=submission_bin_id)

   submission_bin.delete()

   #displays a one-time notification on the page after deleting the submission bin
   messages.success(request, f'Submission Bin has been successfully deleted!')

   return redirect(reverse('pc-submission'))  #the system will direct the user to the current page





# function for creating a notification  after creating submission bin this will notify the faculty
def notify_users(message,user_role_id, program):
  users = CustomUser.objects.filter(role_id=user_role_id).filter(program=program)
  for user in users:
    Notification.objects.create(receipient=user, message=message)





@role_required('Program Chair')
def documents_for_review(request, submission_bin_id):
   submission_bin = get_object_or_404(SubmissionBin, id=submission_bin_id) #get submission_bin_id
   documents = Document.objects.filter(submission_bin=submission_bin).filter(status="Pending").order_by('-date_submitted')  #get all documents submitted in a specific submission_bin in descending order
   return render(request, 'pc/documents_for_review.html', {'submission_bin':submission_bin, 'documents':documents})




@role_required('Program Chair')
def confirm_approve_document(request,document_id):
   document = get_object_or_404(Document, id=document_id)
   submission_bin_id = document.submission_bin.id
   document.status = "Approved"
   document.save()

   #displays a one-time notification on the page after approving the document
   messages.success(request, f'Document {document.document_name} has been approved successfully!')




   #create a record in the notification model
   Notification.objects.create(
      receipient=document.submitted_by,
      message= f'Your document "{document.document_name}" has been approved!'
   )
   return redirect(reverse('documents-for-review', args=[submission_bin_id]))  #the system will direct the user to the documents_for_review page after approving the document.





@role_required('Program Chair')
def confirm_decline_document(request, document_id):
   if request.method == "POST":
     comment = request.POST.get('comment')
     document = get_object_or_404(Document, id=document_id)
     submission_bin_id = document.submission_bin.id
     document.status = "Declined"
     document.comment = comment
     document.save()

   #Creates a one-time notif after declining the document
     messages.success(request, f'Document "{document.document_name}" has been declined.')

   #Creates a record in the Notification model after decling the document
     Notification.objects.create(
      receipient = document.submitted_by,
      message= f'Your document "{document.document_name}" has been declined.'
   )

     return redirect(reverse('documents-for-review', args=[submission_bin_id]))  #the system will direct the user to the documents_for_review page after declining the document.





@role_required('Program Chair')
def view_facultyFiles(request):

  documents = Document.objects.filter(program=request.user.program)

  query = request.GET.get('search', '')
  # this filters the documents by search
  if query:
    documents = documents.filter(Q(document_name__icontains=query)| Q(document_type__icontains=query)| Q(submitted_by__username__icontains=query))


  approved_files = documents.filter(status='Approved').order_by('-date_submitted')
  declined_files = documents.filter(status='Declined').order_by('-date_submitted')
  return render(request, 'pc/Files.html', {'approved_files':approved_files, 'declined_files':declined_files})




# view for viewing pc notifications
@role_required('Program Chair')
def pc_notification_list(request):
  notifications = Notification.objects.filter(receipient=request.user).order_by('-date_created')
  return render(request, 'pc/notification.html', {'notifications':notifications})


# view for changing the read attribute of notification to true
def mark_as_read(request, notification_id):
  notification = get_object_or_404(Notification, id=notification_id)
  notification.read = True
  notification.save()
  return redirect('pc-notifications')



#view for counting unread notification
def unread_notification_count(request):
  unread_count = Notification.objects.filter(receipient=request.user).filter(read=False).count()
  return JsonResponse({'unread_count':unread_count})




