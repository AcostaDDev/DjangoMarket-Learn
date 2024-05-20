from django.contrib import admin

from A_DB.models.shop_models import Category, Product, Image


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ImageItemInLine(admin.TabularInline):
    model = Image
    raw_id_fields = ['product']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'outstanding', 'sold', 'is_artist_product', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available', 'outstanding', 'sold', 'is_artist_product']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ImageItemInLine]
