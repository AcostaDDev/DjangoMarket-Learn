# Generated by Django 5.0.6 on 2024-05-15 19:03

import A_DB.models.shop_models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('A_DB', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to=A_DB.models.shop_models.upload_image_to),
        ),
    ]
