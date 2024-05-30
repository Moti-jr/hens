from django.contrib import admin
from .models import Product

admin.site.site_header = 'Moti Store'

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'stock','price']
    search_fields=('name', 'stock','unit')
    
    
# Register your models here.
from django.contrib import admin
from .models import CustomerProfile, Category, Unit, Product, Order, OrderItem, ShippingAddress

# Register your models here.
admin.site.register(CustomerProfile)
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
