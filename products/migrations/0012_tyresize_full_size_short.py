# Generated by Django 3.2 on 2022-02-10 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_rename_ean_product_ean_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='tyresize',
            name='full_size_short',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
