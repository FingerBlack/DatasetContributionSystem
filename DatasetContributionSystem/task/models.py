from django.db import models
import django.utils.timezone as timezone
from dataset.models import dataset
from user.models import UserProfile

# Create your models here.


class task(models.Model):
    name = models.CharField(max_length=50)
    dataset = models.ForeignKey(dataset, on_delete=models.CASCADE)
    createdTime = models.DateTimeField(default=timezone.now)
    deadline = models.DateField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.BigIntegerField(default=0)
    pv = models.IntegerField()  # 浏览次数


class complete(models.Model):
    task = models.ForeignKey(task, on_delete=models.CASCADE)
    amount = models.BigIntegerField(default=0)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
