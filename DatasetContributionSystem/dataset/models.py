from django.db import models
import django.utils.timezone as timezone
from user.models import UserProfile

# Create your models here.
class dataset(models.Model):
    name = models.CharField(max_length = 50, unique = True)
    createdTime = models.DateTimeField(default = timezone.now)
    owner = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    price = models.FloatField()
    page_view = models.IntegerField(default = 0)
    page_download = models.IntegerField(default = 0)
    size = models.IntegerField(default = 0)
    description = models.CharField(max_length = 200)
    dataType_str = {(1, '带标签的图片'), (2, '无标签的图片')}
    dataType = models.IntegerField(choices = dataType_str)
    cached_time = models.DateTimeField(default = timezone.now)
    last_revise_time = models.DateTimeField(default = timezone.now)
    star = models.IntegerField(default = 0)
    image = models.CharField(max_length = 50, default = '')
    def __str__(self):
        return self.name

class datasetFileIndex(models.Model):
    name = models.ForeignKey(dataset, on_delete = models.CASCADE)
    filename = models.CharField(max_length = 50)
    owner = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    upload_time = models.DateTimeField(default = timezone.now)
    size = models.IntegerField(default = 0)

class transaction(models.Model):
    user1 = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = "transaction_user1")
    user2 = models.ForeignKey(UserProfile, on_delete = models.CASCADE, related_name = "transaction_user2")
    detail = models.CharField(max_length = 50)
    amount = models.FloatField()

class userBuyDataset(models.Model):
    user = models.ForeignKey(UserProfile, on_delete = models.CASCADE)
    dataset = models.ForeignKey(dataset, on_delete = models.CASCADE)