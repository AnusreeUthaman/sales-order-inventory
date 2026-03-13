from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializer import *
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from django.db import transaction
from datetime import datetime
import random
from rest_framework import serializers

# Create your views here.

class ProductCreateListView(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response({
            "success": True,
            "message": "Products retrieved successfully",
            "data":serializer.data,
            },status=status.HTTP_200_OK)
    
    def post(self,request):
        try:
            serializer = ProductSerializer(data=request.data)
            if serializer.is_valid():
                product = serializer.save()

                #create inventory
                Inventory.objects.create(product=product,quantity=0)
                serializer = ProductSerializer(product)

                return Response({
                    "success": True,
                    "message":"Product Created Successfully",
                    "data":serializer.data
                    },status=status.HTTP_201_CREATED)
            
            return Response({
                "success": False,
                "message": "Product creation failed",
                "errors": serializer.errors
                },status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response ({
                "message": "Something went wrong",
                'errors': str(e)
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class ProductDetailView(APIView):
    def get(self,request,id):
        product = get_object_or_404(Product,id=id)
        serializer = ProductSerializer(product)
        return Response({
            "success": True,
            "message": "Product retrieved successfully",
            "data": serializer.data
            }, status=status.HTTP_200_OK)
    
    def put(self,request,id):
        product = get_object_or_404(Product,id=id)

        try:
            serializer = ProductSerializer(product, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "message": "Product updated successfully",
                    "data": serializer.data
                    },status=status.HTTP_200_OK)

            return Response({
                "success": False,
                "message": "Product update failed",
                "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                "message": "Something went wrong",
                "errors": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self,request,id):
        product = get_object_or_404(Product,id=id)
        try:
            product.delete()
            return Response({
                "success": True,
                'message':'product Deleted successfully'
                }, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({
                "message": "Deletion failed",
                "errors": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class DealerCreateListView(APIView):
    def get(self,request):
        dealers = Dealer.objects.all()
        serializer = DealerSerializer(dealers,many=True)
        return Response({
            "success": True,
            "message":"Dealers Retrieved Successfully",
            "data":serializer.data
        },status=status.HTTP_200_OK)

    def post(self,request):
        try:
            serializer=DealerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "message":"Dealer created successfully",
                    "data":serializer.data
                },status=status.HTTP_201_CREATED)
            
            return Response({
                "success": False,
                "message":"Dealer Creation Failed",
                "errors":serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "message":"Something went wrong"
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DealerDetailView(APIView):
    def get(self,request,id):
        dealer = get_object_or_404(Dealer,id=id)
        serializer = DealerSerializer(dealer)
        return Response({
            "success": True,
            "message":"Dealer retrieved Successfully",
            "data":serializer.data
        },status=status.HTTP_200_OK)
    
    def put(self,request,id):
        dealer = get_object_or_404(Dealer,id=id)

        try:
            serializer=DealerSerializer(dealer,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    "success": True,
                    "message":"Dealer updated successfully",
                    "data": serializer.data
                },status=status.HTTP_200_OK)
            
            return Response({
                "success": False,
                "message":"Dealer updation failed",
                "errors":serializer.errors
            },status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                "message": "Something went wrong",
                "errors": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InventoryListView(APIView):
    def get(self,request):
        inventory= Inventory.objects.all()
        serializer=InventorySerializer(inventory,many=True)
        return Response({
            "success": True,
            "message":"Inventory retrieved successfully",
            "data":serializer.data
        },status=status.HTTP_200_OK)

class InventoryUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, product_id):
        inventory = get_object_or_404(Inventory, product_id=product_id)
        quantity = request.data.get("quantity")

        # Validate quantity
        try:
            quantity = int(quantity)
            if quantity < 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response({
                "success": False,
                "message": "Quantity must be a non-negative integer"
            }, status=status.HTTP_400_BAD_REQUEST)

        # Update and save
        inventory.quantity = quantity
        inventory.save()

        return Response({
            "success": True,
            "message": "Stock updated successfully",
            "data": {
                "product_name": inventory.product.name,
                "stock": inventory.quantity
            }
        }, status=status.HTTP_200_OK)
    
class OrderListCreateView(APIView):
    def get(self, request):
        orders = Order.objects.all().order_by('-created_at')

        # Optional filters
        status_filter = request.query_params.get('status')
        dealer_filter = request.query_params.get('dealer')

        if status_filter:
            orders = orders.filter(status=status_filter)

        if dealer_filter:
            orders = orders.filter(dealer_id=dealer_filter)

        serializer = OrderSerializer(orders, many=True)

        return Response({
            "success": True,
            "message": "Orders retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self,request):
        dealer_id = request.data.get('dealer')
        items_data = request.data.get('items',[])

        if not dealer_id or not items_data:
            return Response({"message":"Dealer and items are required"})
        
        with transaction.atomic():
            # create order
            date_part = datetime.now().strftime("%Y%m%d")
            random_part = random.randint(1000,9999)
            order_number = f"ORD-{date_part}-{random_part}"
            order = Order.objects.create(dealer_id=dealer_id,order_number=order_number,status='draft',total_amount=0)

            total_amount = 0
            for item in items_data:
                product_id = item.get('product')
                quantity = item.get('quantity',1)

                if quantity <= 0:
                    raise serializers.ValidationError({"quantity": "Must be greater than 0"})
                
                product = get_object_or_404(Product, id=product_id)
                line_total = product.price * quantity
                total_amount += line_total

                OrderItem.objects.create(order=order, product=product, quantity=quantity, unit_price=product.price, line_total=line_total)
            
            order.total_amount = total_amount
            order.save()

            serializer= OrderSerializer(order)
            return Response({
                "success": True,
                "message":"Draft order Created",
                "data":serializer.data
                },status=status.HTTP_201_CREATED)

class OrderDetailView(APIView):
    def get(self, request, id):
        order = get_object_or_404(Order, id=id)

        serializer = OrderSerializer(order)

        return Response({
            "success": True,
            "message": "Order details retrieved successfully",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def put(self,request,id):
        order = get_object_or_404(Order, id=id)

        if order.status != 'draft':
            return Response({
                "message":"Only draft orders can be edited"
                }, status=status.HTTP_400_BAD_REQUEST)
        
        # Replace Items
        items_data= request.data.get('items',[])
        with transaction.atomic():
            order.items.all().delete() #remove existing items
            total_amount = 0
            for item in items_data:
                product = get_object_or_404(Product, id=item['product'])
                quantity = item.get('quantity', 1)

                if quantity <= 0:
                    raise serializers.ValidationError({"quantity": "Must be greater than 0"})
                
                line_total = product.price * quantity
                total_amount += line_total
                OrderItem.objects.create(order=order, product=product, quantity=quantity, unit_price=product.price, line_total=line_total)

            # Save total amount after processing all items
            order.total_amount = total_amount
            order.save()

            serializer = OrderSerializer(order)
            return Response({
                "success": True,
                "message":"Draft order updated",
                "data":serializer.data
            },status=status.HTTP_200_OK)
        
    def delete(self, request, id):
        order = get_object_or_404(Order, id=id)
        try:
            with transaction.atomic():
                # restore stock if order was confirmed
                if order.status == 'confirmed':
                    for item in order.items.all():
                        inventory = item.product.inventory
                        inventory.quantity += item.quantity
                        inventory.save()
                
                order.delete()

            return Response({
                "success": True,
                "message": "Order deleted successfully"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "success": False,
                "message": "Deletion failed",
                "errors": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class OrderConfirmView(APIView):
    def post(self, request, id):
        order = get_object_or_404(Order, id=id)

        if order.status != 'draft':
            return Response({
                "message": "Only draft orders can be confirmed"
            }, status=status.HTTP_400_BAD_REQUEST)

        # check stock
        insufficient_items = []

        for item in order.items.all():
            if item.quantity > item.product.inventory.quantity:
                insufficient_items.append(
                    f"Insufficient stock for {item.product.name}. "
                    f"Available: {item.product.inventory.quantity}, "
                    f"Requested: {item.quantity}"
                )

        if insufficient_items:
            return Response({
                "detail": insufficient_items
            }, status=status.HTTP_400_BAD_REQUEST)

        # deduct stock
        with transaction.atomic():
            for item in order.items.all():
                inventory = item.product.inventory
                inventory.quantity -= item.quantity
                inventory.save()

            order.status = 'confirmed'
            order.save()

        serializer = OrderSerializer(order)
        return Response({
            "success": True,
            "message": "Order confirmed",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

class OrderDeliverView(APIView):
    def post(self,request,id):
        order = get_object_or_404(Order, id=id)
        
        if order.status != 'confirmed':
            return Response({
                "message":"Only confirmed orders can be delivered"
                },status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'delivered'
        order.save()

        serializer = OrderSerializer(order)
        return Response({
            "success": True,
            "message":"Order delivered",
            "data":serializer.data
        },status=status.HTTP_200_OK)





