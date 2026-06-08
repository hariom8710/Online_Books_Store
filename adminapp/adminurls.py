from django.contrib import admin
from django.urls import path
from .import views
# from mainapp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('admindash/', views.admindash, name='admindash'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('viewenqs/', views.viewenqs, name='viewenqs'),
    path('orders/', views.admin_orders, name='admin_orders'),
    path('customers/', views.admin_customers, name='admin_customers'),
    path('enquiries/', views.admin_enquiries, name='admin_enquiries'),
    path('books/', views.admin_books, name='admin_books'),
    path('delenq/<int:id>/', views.delenq, name='delenq'),
    path('addcat/', views.addcat, name='addcat'),
    path('viewcat/', views.viewcat, name='viewcat'),
    path('addbook/', views.addbook, name='addbook'),
    path('viewbook/', views.viewbook, name='viewbook'),
    path('delcat/<id>/', views.delcat, name='delcat'),
    path('delbook/<id>/', views.delbook, name='delbook'),
    path('change_pwd/', views.change_pwd, name='change_pwd'),
    path('editbook/<id>/', views.editbook, name='editbook'),

]