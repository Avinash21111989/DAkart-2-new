from django.db import models
from django.contrib.auth.models import  User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    addrress_line_1 = models.CharField(max_length=100,blank=True)
    addrress_line_2 = models.CharField(max_length=100,blank=True)
    profile_picture = models.ImageField(upload_to='userprofile',blank=True)
    city = models.CharField(max_length=20,blank=True)
    state = models.CharField(max_length=20,blank=True)
    country = models.CharField(max_length=20,blank=True)

        
    def __str__(self):
        return self.user.first_name
