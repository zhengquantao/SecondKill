from django.db import models

# Create your models here.


class User(models.Model):
    user = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)


class UserToken(models.Model):
    user = models.OneToOneField(to="User")
    token = models.CharField(max_length=64)


class Goods(models.Model):
    number = models.IntegerField(verbose_name='商品号', auto_created=True, primary_key=True, unique=True)
    name = models.CharField(verbose_name='商品名称', max_length=16)
    img = models.CharField(verbose_name='图片链接', max_length=256, null=True)
    price = models.DecimalField(verbose_name='价格', max_digits=6, decimal_places=2)
    detail = models.CharField(verbose_name='详情', max_length=128)
    count = models.IntegerField(verbose_name='数量')
    startTime = models.DateTimeField(verbose_name='开始时间')
    endTime = models.DateTimeField(verbose_name='结束时间')


class Order(models.Model):
    pay_count = models.IntegerField(verbose_name='购买数量')
    user = models.ForeignKey(verbose_name='用户', to='User')
    goods = models.ForeignKey(verbose_name='商品', to='Goods')

    def __str__(self):
        return self.user.user

    class Meta:
        # db_table = "订单表"
        verbose_name = "订单表"
