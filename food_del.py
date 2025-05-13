from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Data model for request body
class Order(BaseModel):
    customer_name: str
    address: str
    items: list[str]
    total_price: float

@app.post("/place-order/")
def place_order(order :Order ):
    return {
        "message":f"order placed successfully for {order.customer_name}",
        "Items" : order.items,
        "total" : order.total_price
    }





from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union, List

app = FastAPI()

# In-memory store for demo
products_db = []

class Feature(BaseModel):
    title: str
    description: str

class Coupon(BaseModel):
    code: str
    amount: float
    expiry: str  # ISO format

class Product(BaseModel):
    name: str
    price: float
    features: List[Feature] = []
    discount: Union[float, Coupon, None] = None

@app.post("/products/")
async def create_product(product: Product):
    products_db.append(product)
    return {
        "message": "Product created successfully",
        "product": product
    }

# ✅ Check inserted products
@app.get("/products/")
async def list_products():
    return {
        "total": len(products_db),
        "products": products_db
    }
