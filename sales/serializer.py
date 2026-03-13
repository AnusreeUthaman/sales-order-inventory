from rest_framework import serializers
from .models import *
from django.core.exceptions import ObjectDoesNotExist

class ProductSerializer(serializers.ModelSerializer):
    # stock = serializers.IntegerField(source='inventory.quantity',read_only=True)
    stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'price', 'stock']
    
    def get_stock(self, obj):
        try:
            return obj.inventory.quantity
        except ObjectDoesNotExist:
            return 0

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ['product', 'quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id','product','quantity','unit_price','line_total']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        fields= ['id','order_number','status','total_amount','created_at','items']

class DealerSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True,read_only=True)

    class Meta:
        model = Dealer
        fields = ['id', 'name','dealer_code', 'email', 'phone', 'address', 'created_at', 'updated_at','orders']

