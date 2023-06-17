import datetime

from django.db import models

# Create your models here.
from register.models import User


class Category(models.Model):
    name_uz = models.CharField(max_length=128)
    name_ru = models.CharField(max_length=128)

    slug = models.CharField(max_length=128)

    def __str__(self):
        return self.name_uz


class Sub_ctg(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name_uz = models.CharField(max_length=128)
    name_ru = models.CharField(max_length=128)

    def __str__(self):
        return self.name_uz


class Product(models.Model):
    sub_ctg = models.ForeignKey(Sub_ctg, on_delete=models.CASCADE)
    name_uz = models.CharField(max_length=128)
    name_ru = models.CharField(max_length=128)

    view = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    dis_like = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name_uz


class Basket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    create_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.price = int(self.product.price) * int(self.quantity)
        return super(Basket, self).save(*args, **kwargs)

    def __str__(self):
        return self.price


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=256)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.first_name


class OTP(models.Model):
    key = models.CharField(max_length=1024, unique=True)
    email = models.CharField(max_length=128)
    is_expired = models.BooleanField(default=False)
    tries = models.SmallIntegerField(default=0)
    state = models.CharField(max_length=128)
    is_confirmed = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now=False, auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def save(self, *args, **kwargs):
        if self.tries >= 5:
            self.is_expired = True

        return super(OTP, self).save(*args, **kwargs)

    def __str__(self):
        return self.OTP.key


class Likes(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)

    def res(self):
        return {
            "product_id": self.product.id,
            "user": self.user.id,
            "like": self.like,
            "dislike": self.dislike,

        }




class Delivery(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=128)
    signed_up = models.BooleanField("Royxatdan otganmi:", default=False)
    agreement = models.BooleanField(default=False)


class Location(models.Model):
    country = models.CharField(max_length=128)
    region = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    location = models.CharField(max_length=128)


class delivery_types(models.Model):
    from_magazine = models.BooleanField()
    from_deliver = models.BooleanField()
    from_comp = models.BooleanField()

class payment_type(models.Model):
    cash = models.BooleanField()
    card = models.BooleanField()
    bank_doc = models.BooleanField()
    kredit = models.BooleanField()
    payment_comp = models.BooleanField()




