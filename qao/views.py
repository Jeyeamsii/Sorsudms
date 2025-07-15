from django.shortcuts import render, get_object_or_404, redirect
from faculty.models import Document
from django.db.models import Q
from dean.decorators import role_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import QAOFile
from .forms import QAOFileUploadForm
from django.template.loader import render_to_string
from django.contrib import messages
from django.http import JsonResponse
from django.http import FileResponse  #designed for streaming files to clients, making it a natural choice for implementing file downloads


# Create your views here.

@role_required('Quality Assurance Officer')
def home_page(request):
  return render(request, 'qao/homepage.html')



@role_required('Quality Assurance Officer')
def all_files(request):

  #get all approved documents
  documents = Document.objects.all().filter(status="Approved")

  query = request.GET.get('search', '')
  # this filters the documents by search
  if query:
    documents = documents.filter(Q(document_type__icontains=query)| Q(submitted_by__username__icontains=query)| Q(program__name__icontains=query)| Q(document_name__icontains=query))


  cict_documents = documents.filter(department__name='CICT')
  cbme_documents = documents.filter(department__name='CBME')


  return render(request,'qao/files.html',{'cict_documents':cict_documents, 'cbme_documents':cbme_documents, 'query':query})



@login_required
def qao_upload_file(request):

    if request.method == 'POST':
        form = QAOFileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            qao_file = form.save(commit=False)
            qao_file.uploaded_by = request.user
            qao_file.save()
            messages.success(request, 'File uploaded successfully!')
            return JsonResponse({"success": True})

        else:
           print(f"Form errors: {form.errors}")
           html_form = render_to_string('pc/upload_file.html',{'form':form}, request=request)
           return JsonResponse({'success':False, 'html_form':html_form})


    else:
        form = QAOFileUploadForm()
    return render(request, 'qao/upload_file.html', {'form': form})





@login_required
def iso_file_view(request):
    qao_files = QAOFile.objects.filter(uploaded_by=request.user).order_by('-date_uploaded')

    query = request.GET.get('search')
    if query:
       qao_files = qao_files.filter(Q(document_name__icontains=query))


    return render(request, 'qao/iso_files.html', {'qao_files': qao_files})



# view that handles viewing iso documents
def document_viewer(request, document_id):
    document = get_object_or_404(QAOFile, id=document_id)
    doc_url = request.build_absolute_uri(document.file.url)
    return render(request, 'qao/document_viewer.html', {'doc_url': doc_url})



# view for downloading approved documents
def download_approved_document(request, document_id):
   #fetch the document instance from the Document model
   document = Document.objects.get(id=document_id)
   document_path = document.file.path

   return FileResponse(open(document_path, 'rb'), as_attachment=True, filename=document.document_name)


# view for downloading iso documents
def download_iso_file(request, document_id):
   #fetch the document instance from the QAOFile model
   document = QAOFile.objects.get(id=document_id)
   document_path = document.file.path

   return FileResponse(open(document_path, 'rb'), as_attachment=True, filename=document.document_name)



def trash_bin(request):
    trashed_documents = QAOFile.trash.all()

    query = request.GET.get('search')
    if query:
       trashed_documents = trashed_documents.filter(Q(document_name__icontains=query))

    return render(request, 'qao/trash_bin.html', {'documents': trashed_documents})


def soft_delete_document(request, document_id):
  document = get_object_or_404(QAOFile, id=document_id)
  document.soft_delete()  # Call the soft delete method
  return redirect('iso-files')  # Redirect to the documents list page


def restore_document(request, document_id):
    document = get_object_or_404(QAOFile.trash, id=document_id)
    document.restore()
    return redirect('trash_binss')


def delete_permanently(request, document_id):
    document = get_object_or_404(QAOFile.trash, id=document_id)
    document.delete_permanently()
    return redirect('trash_binss')

