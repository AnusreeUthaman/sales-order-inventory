from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50,unique=True,db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"
    
class Inventory(models.Model):
    product = models.OneToOneField(Product,on_delete=models.CASCADE,related_name='inventory')
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - stock: {self.quantity}"

class Dealer(models.Model):
    name = models.CharField(max_length=200)
    dealer_code = models.CharField(max_length=50,unique=True,db_index=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ({self.dealer_code})" 

class Order(models.Model):
    STATUS_CHOICES=[
        ('draft', 'Draft'),
        ('confirmed','Confirmed'),
        ('delivered', 'Delivered'),
    ]

    dealer = models.ForeignKey(Dealer,on_delete=models.CASCADE,related_name='orders')
    order_number = models.CharField(max_length=20,unique=True,db_index=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_number} - {self.dealer.name} - {self.status}"
