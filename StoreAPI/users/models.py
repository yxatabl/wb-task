from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)