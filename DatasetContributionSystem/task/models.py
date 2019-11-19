from django.db import models
import django.utils.timezone as timezone
from dataset.models import dataset

# Create your models here.


class task(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    dataset_name = models.ForeignKey(dataset, on_delete=models.CASCADE, related_name="dataset_name")
    createdTime = models.DateTimeField(default=timezone.now)
    pv = models.IntegerField()
    owner = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    task_type = models.CharField(max_length=20)
