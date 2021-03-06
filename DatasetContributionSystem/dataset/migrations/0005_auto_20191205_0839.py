# Generated by Django 2.1.7 on 2019-12-05 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0004_auto_20191204_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='image',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='dataType',
            field=models.IntegerField(choices=[(2, '无标签的图片'), (1, '带标签的图片')]),
        ),
    ]
