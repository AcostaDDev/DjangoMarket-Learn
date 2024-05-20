# Generated by Django 5.0.6 on 2024-05-17 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('A_DB', '0005_alter_image_options_product_genre_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='additional_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='genre',
            field=models.CharField(choices=[('None', 'None'), ('Male', 'Male'), ('Female', 'Female')], default='None', max_length=20, verbose_name='genero'),
        ),
    ]
