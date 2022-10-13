from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    STATUS = (
        (1, 'waiter'),  # ofissant
        (2, 'cashier'),  # kassir
        (3, 'director'),  # director
        (4, 'manager'),  # manager
    )
    type = models.IntegerField(choices=STATUS, default=1)
    works = models.IntegerField(default=0)


class Cash(models.Model):
    status = (
        (1, 'card'),
        (2, 'cash'),
    )
    type = models.IntegerField(choices=status)
    money = models.DecimalField(max_digits=100, decimal_places=2)


class Product(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.BigIntegerField()
    price = models.DecimalField(max_digits=100, decimal_places=2)


class Quitmoney(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class Quitprice(models.Model):
    price = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class Salaryofwaiter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    img = models.ImageField(upload_to='category/')
    name = models.CharField(max_length=210)


class Food(models.Model):
    quantity = models.IntegerField()
    available = models.BooleanField(default=True)
    name = models.CharField(max_length=12121)
    image = models.ImageField(upload_to='images/')
    description = models.CharField(max_length=23232323)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=2)


class Table(models.Model):
    busyness = models.IntegerField(choices=(
        (1, 'Empty'),
        (2, 'Busy'),
    ), default=1)
    number = models.IntegerField()


class OrderItem(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Order(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    order = models.ManyToManyField(OrderItem)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

class Payment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    money = models.DecimalField(max_digits=100, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)