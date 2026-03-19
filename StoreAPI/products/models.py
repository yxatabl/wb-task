from django.db import models


class Product(models.Model):
    name = models.CharField()
    description = models.CharField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()