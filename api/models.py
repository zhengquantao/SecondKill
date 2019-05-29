from django.db import models

# Create your models here.


class User(models.Model):
    user = models.CharField(max_length=16)
    password = models.CharField(max_length=64)


class UserToken(models.Model):
    user = models.OneToOneField(to="User")
    token = models.CharField(max_length=64)


class Goods(models.Model):
    number = models.IntegerField(auto_created=True, primary_key=True, unique=True)
    name = models.CharField(max_length=16)
    img = models.CharField(max_length=256, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    detail = models.CharField(max_length=128)
    count = models.IntegerField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    
    
class Order(models.Model):
    pay_count = models.IntegerField()
    user = models.ForeignKey(to='User')
    goods = models.ForeignKey(to='Goods')
    
    