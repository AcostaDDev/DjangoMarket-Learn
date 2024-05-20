# Generated by Django 5.0.6 on 2024-05-16 14:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('A_DB', '0004_remove_orderitem_quantity_order_phone_number'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'ordering': ['product'], 'verbose_name': 'image', 'verbose_name_plural': 'images'},
        ),
        migrations.AddField(
            model_name='product',
            name='genre',
            field=models.CharField(choices=[('None', 'None'), ('Male', 'Male'), ('Female', 'Female')], default='None', max_length=20, verbose_name='genero'),
        ),
        migrations.AddField(
            model_name='product',
            name='is_artist_product',
            field=models.BooleanField(default=False, verbose_name='producto de artistas'),
        ),
        migrations.AddField(
            model_name='product',
            name='outstanding',
            field=models.BooleanField(default=False, verbose_name='destacado'),
        ),
        migrations.AddField(
            model_name='product',
            name='sold',
            field=models.BooleanField(default=False, verbose_name='vendido'),
        ),
        migrations.AlterField(
            model_name='product',
            name='available',
            field=models.BooleanField(default=True, verbose_name='disponible'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='A_DB.category', verbose_name='categoría'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creado'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, verbose_name='descripción'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='precio'),
        ),
        migrations.AlterField(
            model_name='product',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='actualizado'),
        ),
        migrations.AddIndex(
            model_name='image',
            index=models.Index(fields=['product'], name='A_DB_image_product_222e48_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['outstanding'], name='A_DB_produc_outstan_63d28d_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['sold'], name='A_DB_produc_sold_6d12df_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['is_artist_product'], name='A_DB_produc_is_arti_62bf1a_idx'),
        ),
    ]
