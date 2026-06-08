from django.contrib import admin
from django.urls import path
from .import views
# from mainapp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('userdash/', views.userdash, name='userdash'),
    path('userlogout/', views.userlogout, name='userlogout'),
    path('viewcart/' , views.viewcart, name='viewcart'),
    path('userprofile/', views.userprofile, name='userprofile'),
    path('userorders/', views.userorders, name='userorders'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('user_ch_pwd/', views.user_ch_pwd, name='user_ch_pwd'),
    path('removeitems/<id>',views.removeitems,name='removeitems'),
    path('checkout/',views.checkout, name='checkout'),
    path('payment_success/', views.payment_success, name='payment_success')


    ]