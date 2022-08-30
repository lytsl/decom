from django.db import models
from django.db.models import Min
from django.urls import reverse

from store.models import Product


class Category(models.Model):
    category_name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    category_img = models.ImageField(upload_to='images/categories', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def get_min_price(self):
        product = Product.objects.filter(category=self).aggregate(Min('price'))
        return list(product.values())[0]

    def __str__(self):
        return self.category_name
