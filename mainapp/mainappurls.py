from django.contrib import admin
from django.urls import path
from .import views
from mainapp.views import *
from useraap.views import *
urlpatterns = [
  path('search/', search, name='search'),
    path('admin/', admin.site.urls),
      # Route for the about view
    path('adminlogin/', views.adminlogin, name='adminlogin'),
      path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('service/', service, name='service'),
    path('adminlog/', adminlog, name='adminlog'),
  path('book_details/<id>', book_details, name='book_details'),
  path('addtocart/<int:id>/', addtocart, name='addtocart')
]