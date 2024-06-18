import os
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20)
    password = models.CharField(max_length=128)  # Use a secure hashing algorithm in production
    # confirm_password = models.CharField(max_length=128, null=True, blank=True)
    
    # def clean(self):
    #     if self.password and self.confirm_password and self.password != self.confirm_password:
    #         raise ValidationError(_("The passwords do not match."))

    # @staticmethod
    # def product_list(request):
    #     products = Product.objects.all()
    #     return render(request, 'product_list.html', {'products': products})


def generate_unique_name(instance, filename):
    name = uuid.uuid4()  # universally unique id
    ext = filename.split('.')[-1]
    full_filename = f'{name}.{ext}'  # formating the files
   # full_filename='%s.%s' %(name,ext)
    return os.path.join("pimages", full_filename)


class Category(models.Model):
    """Model for product categories."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    """Model for product units (e.g., grams, liters, etc.)."""
    name = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Product(models.Model):
    """Model for grocery products."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to=generate_unique_name, null=True, blank=True)  # Optional image field
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CustomerProfile(models.Model):
    """Model extending the built-in User model for customer profiles."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

class Order(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)  # Captures order creation time
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)

    @property
    def get_order_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_order_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total

class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=30, null=True)
    zipcode = models.CharField(max_length=30, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
