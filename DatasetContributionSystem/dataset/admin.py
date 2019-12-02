from django.contrib import admin
from .models import dataset, transaction, userBuyDataset

# Register your models here.
admin.site.register(dataset)
admin.site.register(transaction)
admin.site.register(userBuyDataset)