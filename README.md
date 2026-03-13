# Sales Order & Inventory Lite

## Project Overview
This project is a simplified Sales Order & Inventory Management system for auto parts distribution. It allows:

- Admin to manage products, inventory, and dealers
- Dealers to place orders
- Automatic stock management during order confirmation
- Order status flow: Draft → Confirmed → Delivered
- Manual stock adjustment (admin only)
- API-based CRUD operations for products, dealers, orders, and inventory

## Tech Stack

- Language: Python 3.10+
- Framework: Django 4.2+ with Django REST Framework
- Database: PostgreSQL 
- API Format: RESTful JSON

## Setup Instructions

1. Clone the repository:
- git clone https://github.com/AnusreeUthaman/sales-order-inventory.git
- cd sales-order-inventory

2. Create a virtual environment:
python -m venv env
source env/bin/activate # Linux/Mac
env\Scripts\activate # Windows
pip install -r requirements.txt

3. Install dependencies:
- Make sure your virtual environment is activated
- Install all required packages from requirements.txt:
  pip install -r requirements.txt

4. Configure the database (PostgreSQL):
Update `settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sales_inventory_db',   
        'USER': 'postgres',            
        'PASSWORD': 'mypostgres',    
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. Apply migrations:
python manage.py makemigrations
python manage.py migrate

6. Create a superuser
python manage.py createsuperuser

7. Run the development server:
python manage.py runserver

8.Test APIs via Postman
http://127.0.0.1:8000/api/

## API endpoints
### Products
- **GET /api/products/** - List all products
- **POST /api/products/** - Create a new product
  - Example Request:
    ```json
    {
      "name": "Brake Pad",
      "sku": "BP-001",
      "price": 500
    }
    ```
  - Example Response:
    ```json
    {
      "success": true,
      "message": "Product Created Successfully",
      "data": {
        "id": 1,
        "name": "Brake Pad",
        "sku": "BP-001",
        "price": 500,
        "stock": 0
      }
    }
    ```

- **GET /api/products/{id}/** - Get product details  
- **PUT /api/products/{id}/** - Update product  
- **DELETE /api/products/{id}/** - Delete product  

### Dealers
- **GET /api/dealers/** - List all dealers  
- **POST /api/dealers/** - Create a new dealer 
- Example Request:
    ```json
    {
        "name": "ABC Motors",
        "dealer_code": "ABC123",
        "email": "abc@example.com",
        "phone": "9876543210",
        "address": "123 Main Street, City"
    }
    ```

- Example Response:
```json
    {
    "success": true,
    "message": "Dealer created successfully",
    "data": {
        "id": 1,
        "name": "ABC Motors",
        "dealer_code": "ABC123",
        "email": "abc@example.com",
        "phone": "9876543210",
        "address": "123 Main Street, City",
        "created_at": "2026-03-13T08:50:00.123456Z",
        "updated_at": "2026-03-13T08:50:00.123456Z",
        "orders": []
    }
    }

```
- **GET /api/dealers/{id}/** - Get dealer details with orders  
- **PUT /api/dealers/{id}/** - Update dealer  

### Orders
- **GET /api/orders/** - List all orders  
- **POST /api/orders/** - Create draft order 
- Example Request:
```json 
{
  "dealer": 1,
  "items": [
    {
      "product": 1,
      "quantity": 10
    }
  ]
}
```
- Example Response:
```json
{
  "success": true,
  "message": "Draft order Created",
  "data": {
    "id": 1,
    "order_number": "ORD-20260313-1056",
    "status": "draft",
    "total_amount": "5000.00",
    "created_at": "2026-03-13T08:55:00.123456Z",
    "items": [
      {
        "id": 1,
        "product": 1,
        "quantity": 10,
        "unit_price": "500.00",
        "line_total": "5000.00"
      }
    ]
  }
}
```
- **POST /api/orders/{id}/confirm/** – Insufficient stock scenario
- Example Response:
```json
{
    "detail": [
        "Insufficient stock for Brake Pad. Available: 5, Requested: 10",
        "Insufficient stock for Oil Filter. Available: 2, Requested: 5"
    ]
}
```
- **GET /api/orders/{id}/** - Get order with items  
- **PUT /api/orders/{id}/** - Update draft order  
- **POST /api/orders/{id}/confirm/** - Confirm order (validates stock)  
- Example Response:
```json
{
  "success": true,
  "message": "Order confirmed",
  "data": {
    "id": 1,
    "order_number": "ORD-20260313-1056",
    "status": "confirmed",
    "total_amount": "5000.00",
    "created_at": "2026-03-13T08:55:00.123456Z",
    "items": [
      {
        "id": 1,
        "product": 1,
        "quantity": 10,
        "unit_price": "500.00",
        "line_total": "5000.00"
      }
    ]
  }
}
```
- **POST /api/orders/{id}/deliver/** - Mark as delivered  

### Inventory (Admin Only)
- **GET /api/inventory/** - List all inventory levels  
- **PUT /api/inventory/{product_id}/** - Update stock manually (admin only)  
- Example Request:
```json 
{
  "quantity": 100
}
```
- Example Response:
```json
{
  "success": true,
  "message": "Stock updated successfully",
  "data": {
    "product_name": "Brake Pad",
    "stock": 100
  }
}
```
> Include example JSON requests/responses for each, similar to above.

## Database Schema Diagram

Product
-------
id (PK)
name
sku (unique)
description
price
created_at
updated_at

Inventory
---------
id (PK)
product_id (FK -> Product, One-to-One)
quantity
updated_at

Dealer
------
id (PK)
name
dealer_code (unique)
email (unique)
phone
address
created_at
updated_at

Order
-----
id (PK)
dealer_id (FK -> Dealer)
order_number (unique)
status (Draft / Confirmed / Delivered)
total_amount
created_at
updated_at

OrderItem
-----
id (PK)
order_id (FK -> Order)
product_id (FK -> Product)
quantity
unit_price
line_total
created_at
updated_at

## Assumptions Made
- Each product automatically gets an inventory record with 0 stock upon creation.
- Only admin users can manually update stock.
- Order total_amount and line_total are automatically calculated.
- Stock is only deducted when an order is confirmed.
- Draft orders can be updated; Confirmed/Delivered orders cannot be edited.
- Order numbers are auto-generated in the format: ORD-YYYYMMDD-RANDOM.

## Postman Collection

All APIs are included in the Postman collection for easy testing:

- File: `sales_inventory.postman_collection.json`
- Import it in Postman to test all endpoints
- Admin token is required for inventory updates