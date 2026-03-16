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
    cart = models.OneToOneField(
        Cart,
        on_delete=models.CASCADE
    )
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)