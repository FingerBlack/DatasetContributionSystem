# Generated by Django 2.1.7 on 2019-12-03 06:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Description', models.CharField(max_length=1000)),
                ('Score', models.IntegerField()),
                ('Time', models.DateTimeField(default=django.utils.timezone.now)),
                ('Like', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='star',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
