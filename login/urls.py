from django.urls import path
from . import views

urlpatterns = [
  path('', views.login_view, name='login'),
  path('logout/', views.log_out, name='Logout')
]