from django.db import models
import django.utils.timezone as timezone
# Create your models here.
class comment(models.Model):
    DatasetName = models.CharField(max_length = 50, primary_key = True)
    Username = models.CharField(max_length = 50)
    Description = models.CharField(max_length = 1000)
    Score = models.IntegerField()
    Time = models.DateTimeField(default = timezone.now)