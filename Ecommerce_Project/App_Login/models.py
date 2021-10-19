from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_profile')
    
    full_name = models.CharField(max_length=264,blank=True)
    address_1 = models.CharField(max_length=264, blank=True)
    city = models.CharField(max_length=264 , blank=True)
    zipcode = models.CharField(max_length=10,blank=True)
    country = models.CharField(max_length=50,blank=True)
    phone = models.CharField(max_length=20,blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    profile_pic = models.ImageField(upload_to='profile_pics')
