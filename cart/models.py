from django.db import models


class Cart(models.Model):
    cart_id = models.CharField(max_length=200, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def add(self):
        self.quantity += 1

    def image_url(self):
        return self.product.images.first.image.url

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product
