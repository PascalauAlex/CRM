from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE

from core.models import Address


# Create your models here.





class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='userprofile')
    phone = models.CharField(max_length=15,blank=True)
    full_name = models.CharField(max_length=255,blank=True)
    profile_picture = models.ImageField(upload_to='userprofile/profile_picture/', blank=True, null=True)
    date_of_birth = models.DateTimeField(blank=True,null=True)
    google_refresh_token = models.CharField(max_length=255, blank=True, null=True)
    user_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name='userprofile_address', null=True, blank=True)
    picture_url = models.URLField(blank=True,null=True)
    profile_completed = models.BooleanField(default=False)
    

    def __str__(self):
        return f"{self.user.username} + ' ' + {self.full_name}"









