

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

fake_items_db = [
    {"item_name": "Apple", "category": "fruit", "price": 10},
    {"item_name": "Banana", "category": "fruit", "price": 5},
    {"item_name": "Milk", "category": "dairy", "price": 30},
    {"item_name": "Bread", "category": "bakery", "price": 25},
    {"item_name": "Cheese", "category": "dairy", "price": 40},
]

class Item(BaseModel):
    item_name: str
    category: str
    price: float

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    if 0 <= item_id < len(fake_items_db):
        fake_items_db[item_id] = item.dict()
        return {"message": "Item updated", "item": item}
    return {"error": "Invalid item ID"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    if 0 <= item_id < len(fake_items_db):
        return fake_items_db[item_id]
    return {"error": "Invalid item ID"}
