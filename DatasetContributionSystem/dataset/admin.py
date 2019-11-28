from django.contrib import admin
from .models import dataset, transaction

# Register your models here.
admin.site.register(dataset)
admin.site.register(transaction)