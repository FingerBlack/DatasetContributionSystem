from django.db import models
import django.utils.timezone as timezone
from dataset.models import dataset
from user.models import UserProfile

# Create your models here.
class comment(models.Model):
    DatasetName = models.ForeignKey(dataset,on_delete=models.CASCADE)
    Username = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    Description = models.CharField(max_length = 1000)
    Score = models.IntegerField()
    Time = models.DateTimeField(default = timezone.now)
    Like = models.IntegerField(default = 0)

class star(models.Model):
    DatasetName = models.ForeignKey(dataset, on_delete=models.CASCADE, related_name = "star_dn")
    Username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
