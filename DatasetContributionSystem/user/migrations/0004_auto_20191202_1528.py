# Generated by Django 2.2.7 on 2019-12-02 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20191202_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='icon',
            field=models.CharField(default='/static/default.jpg', max_length=500),
        ),
    ]
