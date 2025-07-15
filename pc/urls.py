from django.urls import path
from . import views

urlpatterns = [
  path("homepage/", views.homepage, name="pc-homepage"),
  path("submission/", views.submission, name='pc-submission'),
  path('files/', views.view_facultyFiles, name='pc-files'),
  path('submission/create-submission/', views.create_submission_bin, name='create_submission_bin'),
  path('submission/edit-submission-bin/<int:user_bin_id>/', views.edit_submission_bin, name='edit_submission_bin'),
  path('submission/delete-submission-bin/<int:submission_bin_id>/', views.confirm_delete_submission_bin, name="delete_submission_bin"),
  path('submission/<int:submission_bin_id>/documents/', views.documents_for_review, name='documents-for-review'),
  path('documents/confirm-approval/<int:document_id>/', views.confirm_approve_document, name='confirm-document-approval'),
  path('documents/confirm-decline/<int:document_id>/', views.confirm_decline_document, name='confirm-document-decline'),
  path('notifications/', views.pc_notification_list, name='pc-notifications'),
  path('notifications/mark-as-read/<int:notification_id>/', views.mark_as_read, name='mark-as-reads'),
  path('notifications/count', views.unread_notification_count, name='unread-notification-count'),

]