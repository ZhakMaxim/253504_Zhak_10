from django.db import models
from django.contrib.auth.models import AbstractUser
import re
from django.core.exceptions import ValidationError

class User(AbstractUser):
    STATUS_CHOICES = (
        ("employee", "employee"),
        ("customer", "customer"),
    )
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="customer")
    phone_number = models.CharField(max_length=13)

    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        phone_number_pattern = re.compile(r'\+375(25|29|33)\d{7}')
        if not re.fullmatch(phone_number_pattern, str(self.phone_number)):
            raise ValidationError("This field accepts mail id of google only")
        super().save(*args, **kwargs)

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
    price = models.FloatField()
    amount = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    number = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, related_name='orders', on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(default=1)
    price = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)