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
    class Genre(models.Choices):
        none = 'None'
        male = 'Male'
        female = 'Female'

    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='categoría')
    name = models.CharField(max_length=200, verbose_name='nombre')
    slug = models.SlugField(max_length=200)
    description = models.TextField(blank=True, verbose_name='descripción')
    genre = models.CharField(choices=Genre.choices, default=Genre.none, max_length=20, verbose_name='genero')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='precio')
    available = models.BooleanField(default=True, verbose_name='disponible')
    created = models.DateTimeField(auto_now_add=True, verbose_name='creado')
    updated = models.DateTimeField(auto_now=True, verbose_name='actualizado')
    outstanding = models.BooleanField(default=False, verbose_name='destacado')
    sold = models.BooleanField(default=False, verbose_name='vendido')
    is_artist_product = models.BooleanField(default=False, verbose_name='producto de artistas')

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['outstanding']),
            models.Index(fields=['sold']),
            models.Index(fields=['is_artist_product']),
            models.Index(fields=['-created']),
        ]

        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug, self.id])

    def get_image_url(self):
        return self.images.first().image.url


class Image(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_image_to, null=True, blank=True)

    class Meta:
        ordering = ['product']
        indexes = [
            models.Index(fields=['product']),
        ]
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def __str__(self):
        return self.product.name

