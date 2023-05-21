from django.contrib import admin
from .models import User, UserList, Product, ProductList

# Register your models here.
admin.site.register(User, UserList)
admin.site.register(Product, ProductList)
