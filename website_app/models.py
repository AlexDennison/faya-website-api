from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractUser



# Create your models here.


class User(AbstractUser):
    address = models.TextField()
    phone = models.TextField()


class UserList(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'address', 'phone')


class Product(models.Model):
    product_name = models.TextField()
    product_code_number = models.TextField(unique=True)
    buildup_date = models.DateTimeField(auto_now_add=True)
    product_price = models.FloatField(default=0)
    product_quantity = models.IntegerField(default=0)
    product_status = models.BooleanField(default=True)
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.product_code_number

    def generate_code_number(self):
        latest_product = Product.objects.all().order_by('-id').first()
        if latest_product:
            new_code_number = str(int(latest_product.product_code_number[4:]) + 1).zfill(4)
            return f"PRO-{new_code_number}"
        else:
            return "PRO-0001"

    def save(self, *args, **kwargs):
        if not self.product_code_number:
            product_code_number = self.generate_code_number()
            self.product_code_number = product_code_number
        super().save(*args, **kwargs)


class ProductList(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_code_number', 'buildup_date',
                    'product_price', 'product_quantity', 'product_status', 'owner_id')
