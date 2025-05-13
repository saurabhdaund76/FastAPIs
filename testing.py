from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# Sample DB
fake_items_db = [
    {"item_name": "Apple", "category": "fruit", "price": 10},
    {"item_name": "Banana", "category": "fruit", "price": 5},
    {"item_name": "Milk", "category": "dairy", "price": 30},
    {"item_name": "Bread", "category": "bakery", "price": 25},
    {"item_name": "Cheese", "category": "dairy", "price": 40},
]


# POST with Pydantic model
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

@app.post("/items/")
async def create_item(item: Item):
    return item



# POST for search filters
class SearchFilters(BaseModel):
    name: Optional[str] = None
    max_price: Optional[float] = None

@app.post("/items/search")
async def search_items(filters: SearchFilters):
    results = fake_items_db
    if filters.name:
        results = [item for item in results if filters.name.lower() in item["item_name"].lower()]
    if filters.max_price is not None:
        results = [item for item in results if item["price"] <= filters.max_price]
    return {"results": results}

