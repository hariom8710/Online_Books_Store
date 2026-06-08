from django.db import models

# Create your models here.
class Enquiry(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contactnumber=models.CharField(max_length=15)
    subject= models.CharField(max_length=200)
    message= models.TextField()
    enqdate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f" Enquiry of {self.name} - {self.contactnumber}"

class LoginInfo(models.Model):
    usertype= models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='active')
    def __str__(self):
        return f"{self.username} -{self.usertype}"

class UserInfo(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    contactnumber = models.CharField(max_length=15)
    address = models.TextField()
    profile = models.ImageField(upload_to='profiles/', blank=True, null=True)
    login = models.OneToOneField(LoginInfo, on_delete=models.CASCADE, )
    created_at = models.DateTimeField(auto_now_add=True)
