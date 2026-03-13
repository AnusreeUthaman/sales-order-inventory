from django.urls import path
from .views import *

urlpatterns=[

    #products
    path('products/',ProductCreateListView.as_view(),name='product-list-create'),
    path('products/<int:id>/',ProductDetailView.as_view(),name='product-detail'),

    #dealers
    path('dealers/',DealerCreateListView.as_view(), name="dealer-list-create"),
    path('dealers/<int:id>/',DealerDetailView.as_view(),name='dealer-list'),

    #inventory
    path('inventory/',InventoryListView.as_view(),name='inventory-list'),
    path('inventory/<int:product_id>/',InventoryUpdateView.as_view(),name='inventory-update'),

    #orders
    path('orders/',OrderListCreateView.as_view(),name='order-list-create'),
    path('orders/<int:id>/',OrderDetailView.as_view(),name='order-detail'),
    path('orders/<int:id>/confirm/',OrderConfirmView.as_view(),name='order-confirm'),
    path('orders/<int:id>/deliver/',OrderDeliverView.as_view(),name='order-deliver'),
    
]