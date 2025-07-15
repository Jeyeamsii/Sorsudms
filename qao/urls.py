from django.urls import path
from . import views

urlpatterns = [
  path('', views.home_page, name='qao-homepage'),
  path('files', views.all_files, name='all-approved-files'),
  path('iso-files/', views.iso_file_view, name='iso-files'),
  path('iso-files/upload', views.qao_upload_file, name='file-upload'),
  path('document-viewer/<int:document_id>/', views.document_viewer, name="document_viewer"),
  path('download/<int:document_id>/', views.download_approved_document, name='download-document'),
  path('download-iso-files/<int:document_id>/', views.download_iso_file, name='download-iso-file'),
  path('documents/<int:document_id>/soft-delete/', views.soft_delete_document, name='soft_delete_iso_documents'),
  path('trash/', views.trash_bin, name='trash_binss'),
  path('restore/<int:document_id>/', views.restore_document, name='restore_iso_documents'),
  path('delete/<int:document_id>/', views.delete_permanently, name='delete_document_permanently'),
]