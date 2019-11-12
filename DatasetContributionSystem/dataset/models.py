from django.db import models

# Create your models here.
class dataset(models.Model):
    name = models.CharField(max_length = 50, primary_key = True)
    createdTime = models.DateTimeField()
    pv = models.IntegerField() #浏览次数
    owner = models.CharField(max_length = 50)
    price = models.FloatField()
    dataType_str = {(1, '图像')}
    dataType = models.IntegerField(choices = dataType_str)
