import os
from django.core.exceptions import ValidationError

def validate_size_and_type(file):
  allowed_extensions = ['.docx', '.xlsx', '.pdf', '.ppt', '.pptx']
  if not any(file.name.endswith(ext) for ext in allowed_extensions):
        raise ValidationError(f"Only the following file types are allowed: {', '.join(allowed_extensions)}")
  #check the file size
  file_size = file.size
  max_size = 20 * 1024 * 1024 #20MB in bytes
  if file_size > max_size:
    raise ValidationError('File size cannot exceed 20MB.')