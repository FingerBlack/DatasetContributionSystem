# Generated by Django 2.1.7 on 2019-12-03 06:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('createdTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('price', models.FloatField()),
                ('page_view', models.IntegerField(default=0)),
                ('page_download', models.IntegerField(default=0)),
                ('size', models.IntegerField(default=0)),
                ('description', models.CharField(max_length=200)),
                ('dataType', models.IntegerField(choices=[(1, '带标签的图片'), (2, '无标签的图片')])),
                ('cached_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_revise_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('star', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='datasetFileIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=50)),
                ('upload_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('size', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='userBuyDataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataset.dataset')),
            ],
        ),
    ]
