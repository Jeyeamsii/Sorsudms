from django.db import models
from django.contrib.auth.models import AbstractUser  #a class provided by django that serves as a base class for custom user models. It provides the foundation for creating a custom user model that extends Django's built-in user model

from .validators import validate_image


# Create your models here.

class Department(models.Model):
  name = models.CharField(max_length=4)

  def __str__(self):
    return self.name  #The __str__ function in Python is a special method that returns a string representation of an object.


class Role(models.Model):
  name = models.CharField(max_length=30)


  def __str__(self):
    return self.name


class Program(models.Model):
  name = models.CharField(max_length=6, null=True)
  department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

  def __str__(self):
    return self.name


# creating a custom user with added fields
# add 'from django.contrib.auth.models import Abstractuser' at the top
class CustomUser(AbstractUser):
  address = models.CharField(max_length=255, null=True, blank=True)
  birthday = models.DateField(null=True, blank=True)
  middle_initial = models.CharField(max_length=1, null=True, blank=True)
  role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
  department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
  program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
  bio = models.TextField(blank=True, null=True)
  profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True, validators=[validate_image])
  is_archived = models.BooleanField(default=False)


  # if the is_archived is True, this automatically set the is_active attribute to false
  # returns a typerror if *args and **kwargs are omitted because this allow the method to accept all the standard parameters
  def save(self, *args, **kwargs):
    if self.is_archived:
      self.is_active = False
    super().save(*args, **kwargs)



