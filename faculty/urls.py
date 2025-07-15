from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='faculty-homepage'),
    path('files/', views.files_view, name='faculty-files'),
    path('SubmissionBin/', views.submissionBinList, name='submission-bin-list'),
    path('generalSubmissionBin/submit-document/<int:submission_bin_id>/', views.submit_document, name='submit_document'),
    path('notifications/', views.faculty_notification_list, name='faculty-notifications'),
    path('notifications/mark-as-rad/<int:notification_id>/', views.mark_as_read, name='mark-as-read'),
    path('notifications/count', views.unread_notification_count, name='unread-notification-count'),
    path('document-viewer/<int:document_id>/', views.document_viewer, name="document-viewer"),
    path('documents/<int:document_id>/soft-delete/', views.soft_delete_document, name='soft_delete_document'),
    path('trash/', views.trash_bin, name='trash_bin'),
    path('restore/<int:document_id>/', views.restore_document, name='restore_document'),
    path('delete/<int:document_id>/', views.delete_permanently, name='delete_permanently'),

]