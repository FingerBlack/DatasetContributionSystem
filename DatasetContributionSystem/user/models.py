from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.

class UserProfile(AbstractUser):
    description = models.CharField(max_length = 500, blank=True) 
    balance = models.FloatField(default = 0.0)
    avatar = models.CharField(max_length = 500, default = '', blank = True)
