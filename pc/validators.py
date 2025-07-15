from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from django.core.exceptions import ValidationError

def validate_deadline(value):
  if value < timezone.now():
    raise ValidationError('The deadline cannot be in the past')
  
def validate_academic_year(value):
  pattern = re.compile(r'^\d{4}-\d{4}$')
  if not pattern.match(value):
    raise ValidationError('Invalid academic year format.')
  start_year, end_year = map(int, value.split('-'))
  if end_year != start_year + 1:
    raise ValidationError('End year must be one year after the start year')