from django.db import models
import django.utils.timezone as timezone
from dataset.models import dataset

# Create your models here.


class task(models.Model):
    name = models.CharField(max_length=50)
    dataset = models.ForeignKey(dataset, on_delete=models.CASCADE)
    createdTime = models.DateTimeField(default=timezone.now)
    deadline = models.DateField()
    owner = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    amount = models.BigIntegerField(default=0)
    pv = models.IntegerField()  # 浏览次数
