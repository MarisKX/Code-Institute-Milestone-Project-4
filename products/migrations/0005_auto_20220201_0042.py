# Generated by Django 3.2 on 2022-02-01 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20220130_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='load_index',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='speed_index',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]
