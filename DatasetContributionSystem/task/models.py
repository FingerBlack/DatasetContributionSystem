from django.db import models
import django.utils.timezone as timezone
from dataset.models import dataset

# Create your models here.


class task(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    # name = models.ForeignKey(dataset, on_delete=models.CASCADE, related_name="related_dataset")
    related_dataset = models.CharField(max_length=50)
    createdTime = models.DateTimeField(default=timezone.now)
    deadline = models.DateField()
    owner = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    amount = models.BigIntegerField(default=0)
    pv = models.IntegerField()  # 浏览次数
