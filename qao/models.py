from django.db import models
from dean.models import CustomUser
from faculty.validators import validate_size_and_type
from datetime import timedelta
from django.utils.timezone import now


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

class TrashManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=False)




# Create your models here.
class QAOFile(models.Model):
  file = models.FileField(upload_to='documents/', validators=[validate_size_and_type])
  uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  date_uploaded = models.DateTimeField(auto_now=True)
  document_name = models.CharField(max_length=255)
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
    expired_documents = QAOFile.trash.filter(deleted_at__lt=now() - timedelta(days=30))
    for doc in expired_documents:
        doc.delete_permanently()






