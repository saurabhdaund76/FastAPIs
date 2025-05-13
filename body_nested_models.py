from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Product(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []  # List of strings representing product tags


@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    return {
        "message": "Product updated successfully",
        "product_id": product_id,
        "product_data": product
    }




# all the things together with real world ex 

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Union

app = FastAPI()


class Feature(BaseModel):
    title: str
    description: str


class Coupon(BaseModel):
    code: str
    amount: float
    expiry: str  # in ISO format like "2025-12-31"


class Product(BaseModel):
    name: str
    price: float
    features: list[Feature] = []
    discount: Union[float, Coupon, None] = None  # Can be a float, a Coupon, or None


@app.post("/products/")
async def create_product(product: Product):
    return {
        "message": "Product created successfully",
        "product": product
    }


# create a method to check if the data is successfully inserted or not!