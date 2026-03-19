from django.db import models

from users.models import User

from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        name='user'
    )


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='products'
    )
    quantity = models.PositiveIntegerField(default=1)


    class Meta:
        unique_together = ['cart', 'product']