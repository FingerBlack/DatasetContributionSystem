from django.db import models

# Create your models here.
class comment(models.Model):
    DatasetName = models.CharField(max_length = 50, primary_key = True)
    Username = models.CharField(max_length = 50)
    Description = models.IntegerField()
    Score = models.BooleanField()
    Time = models.DateTimeField()