import os

from django.utils import timezone
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


def upload_image_to(instance, filename):
    name, ext = os.path.splitext(filename)  # Separar el nombre del archivo y la extensión
    folder = 'shop/products'  # Carpeta principal donde se guardarán las imágenes
    product_name = instance.product.name  # Obtener el nombre del producto
    now = timezone.now()  # Obtener la fecha y hora actual
    date_path = now.strftime('%Y/%m/%d')  # Formatear la fecha como año/mes/día
    new_filename = f'{product_name}{ext}'  # Nuevo nombre del archivo con el nombre del producto
    return os.path.join(folder, date_path, product_name, new_filename)  # Devolver la ruta completa del archivo


class Product(models.Model):

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug, self.id])


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_to, null=True, blank=True)

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def __str__(self):
        return self.product.name

