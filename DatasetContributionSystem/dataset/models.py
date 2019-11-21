from django.db import models
import django.utils.timezone as timezone

# Create your models here.
class dataset(models.Model):
    name = models.CharField(max_length = 50, primary_key = True)
    createdTime = models.DateTimeField(default = timezone.now)
    pv = models.IntegerField() #浏览次数
    owner = models.CharField(max_length = 50)
    price = models.FloatField()
    size = models.IntegerField(default = 0)
    description = models.CharField(max_length = 200)
    dataType_str = {(1, '分类'), (2, '检测')}
    dataType = models.IntegerField(choices = dataType_str)

class datasetFileIndex(models.Model):
    name = models.ForeignKey(dataset, on_delete=models.CASCADE, related_name="dataset_name")
    filename = models.CharField(max_length = 50)