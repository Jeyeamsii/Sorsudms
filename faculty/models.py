from django.db import models
from pc.models import SubmissionBin
from dean.models import CustomUser, Department, Program
from .validators import validate_size_and_type
from datetime import timedelta
from django.utils.timezone import now


# Create your models here.

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class TrashManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=False)



class Document(models.Model):

  submission_bin = models.ForeignKey(SubmissionBin, on_delete=models.CASCADE)
  submitted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  file = models.FileField(upload_to='documents/', validators=[validate_size_and_type])
  date_submitted = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=30, choices=[('Pending','Pending'),('Approved','Approved'),('Declined','Declined')])
  comment = models.TextField(blank=True, null=True)
  document_type = models.CharField(max_length=100)
  document_name = models.CharField(max_length=255)
  department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
  program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True)
  deleted_at = models.DateTimeField(null=True, blank=True)



  def __str__(self):
        return self.name

  def is_deleted(self):
      return self.deleted_at is not None

  def is_expired(self):
      if self.deleted_at:
          return now() > self.deleted_at + timedelta(days=30)
      return False

  # soft delete method. When you call delete() on a document, it will now set the deleted_at timestamp instead of removing the object.
  def soft_delete(self, *args, **kwargs):
        self.deleted_at = now()
        self.save()

  objects = ActiveManager()
  trash = TrashManager()

  def restore(self):
        self.deleted_at = None
        self.save()

  def delete_permanently(self):
        super().delete()  # Call the parent method for hard deletion

  def delete_expired_documents():
    expired_documents = Document.trash.filter(deleted_at__lt=now() - timedelta(days=30))
    for doc in expired_documents:
        doc.delete_permanently()



