from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Role,Department, Program

# Register your models here.
class CustomUserAdmin(UserAdmin):
  list_display = ('username','email','role','department')  #specifies which fields of the model should be displayed in the list view of the admin interface
  fieldsets = (
    (None, {'fields':('username','password','email','role','department','program')}),
    ('Personal Info',{'fields':('first_name','last_name','middle_initial','birthday','address')}),
    ('Important Dates',{'fields':('last_login','date_joined')})
  )      # fieldsets is used to control the layout of the fields in the detail view




#register the model and admin class
admin.site.register(CustomUser,CustomUserAdmin)

admin.site.register(Role)
admin.site.register(Department)
admin.site.register(Program)
