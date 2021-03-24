from django.db import models
import time
import uuid
from rest_framework import serializers


class User(models.Model):
    user_name = models.CharField(max_length=200)
    user_id =  models.CharField(max_length=200,default=uuid.uuid1,unique=True)
    user_address = models.CharField(max_length=100)
    user_image = models.ImageField(upload_to ='Faces/{}'.format(time.strftime("%Y-%m-%d-%H-%M-%S")))
    user_phone = models.CharField(max_length=20,default="")
    user_email = models.CharField(max_length=100,default="")
    order_count = models.IntegerField(default=0) 

    def __str__(self):
        return self.user_name

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class Product(models.Model):
    title = models.CharField(max_length=1000)
    product_id = models.CharField(max_length=1000,default=uuid.uuid4,unique=True)
    price = models.IntegerField(default=0) 
    category = models.CharField(max_length=100) 
    logo = models.CharField(max_length=100000)
    description = models.CharField(max_length=10000)
    weight = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)    
    def __str__(self):
        return self.title

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    order_id = models.CharField(max_length=1000)
    product_quantity = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.user_name + "-" + self.order_id

class Discount(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    percent = models.IntegerField(default=0)
    emailed = models.BooleanField(default=False)
    def __str__(self):
        return self.product.title

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
