from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Dealer)
admin.site.register(Order)
admin.site.register(OrderItem)