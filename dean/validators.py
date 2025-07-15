
#file that stores all custom validator that can be used throughout the project.
#this custom validators can be used in validating models and forms

from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import re #provides support for regular expressions which are powerful tools for matching patterns in strings


#validate birthday where it must not be in future
def validate_birthday(value):
  if value > timezone.now().date():
    raise ValidationError("Birthday cannot be in the future.")
  
  #Calculate the minimum date for being 23 years old
  min_date = timezone.now().date() - timedelta(days=365*18)
  if value > min_date:
    raise ValidationError("Must be at least 23 years old")
  

def validate_letters_only(value):
  if not re.match(r'^[a-zA-Z\s]+$',value):
    raise ValidationError('This field must contain only letters.')
  

def validate_image(value):
  if not value.name.endswith(('.jpg','.jpeg','.png')):
    raise ValidationError('Only .jpg, .jpeg, and .png files are allowed.')