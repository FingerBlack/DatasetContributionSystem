# Generated by Django 2.2.7 on 2019-12-02 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dataset', '0003_auto_20191202_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='dataType',
            field=models.IntegerField(choices=[(2, '无标签的图片'), (1, '带标签的图片')]),
        ),
    ]
