from django.db import models
import django.utils.timezone as timezone
from dataset.models import dataset

# Create your models here.
class Lists(models.Model):
    name_list=dataset.objects.all().filter(name__contains = 1)