from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    STATUS_CHOICES = (
        ("employee", "employee"),
        ("customer", "customer"),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="customer")

    def __str__(self):
        return self.first_name


class Producer(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ManyToManyField(Category, related_name='products')
    producer = models.ForeignKey(Producer, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    number = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
