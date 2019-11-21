from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class comment(models.Model):
    DatasetName = models.CharField(max_length = 50, primary_key = True)
    Username = models.CharField(max_length = 50)
    Description = models.CharField(max_length = 50)
    Score = models.BooleanField()
    Time = models.DateTimeField()