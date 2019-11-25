from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class dataset(models.Model):
    name = models.CharField(max_length = 50, primary_key = True)
    createdTime = models.DateTimeField(default = timezone.now)
    owner = models.CharField(max_length = 50)
    price = models.FloatField()
    page_view = models.IntegerField(default = 0)
    page_download = models.IntegerField(default = 0)
    size = models.IntegerField(default = 0)
    description = models.CharField(max_length = 200)
    dataType_str = {(1, '分类'), (2, '检测')}
    dataType = models.IntegerField(choices = dataType_str)
    cached_time = models.DateTimeField(default = timezone.now)
    last_revise_time = models.DateTimeField(default = timezone.now)

class datasetFileIndex(models.Model):
    name = models.ForeignKey(dataset, on_delete=models.CASCADE)
    filename = models.CharField(max_length = 50)

class datasetStatistic(models.Model):
    dataset = models.OneToOneField(dataset, on_delete=models.CASCADE)