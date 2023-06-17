from django.contrib import admin

# Register your models here.
from sayt.models import Category, Sub_ctg, Product, Basket, Comment, OTP
from register.models import User

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Sub_ctg)
admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(Comment)
admin.site.register(OTP)
