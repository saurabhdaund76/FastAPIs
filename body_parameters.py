#  you're now diving into one of the most powerful features of FastAPI: 
# combining path parameters, query parameters, and body parameters (with Pydantic models) 
# in the same API call. Let me walk you through this step-by-step, using our grocery store example to make 
# it super practical.

fake_items_db = {
    0: {"item_name": "Apple", "category": "fruit", "price": 10},
    1: {"item_name": "Banana", "category": "fruit", "price": 5},
    2: {"item_name": "Milk", "category": "dairy", "price": 30},
    3: {"item_name": "Bread", "category": "bakery", "price": 25},
    4: {"item_name": "Cheese", "category": "dairy", "price": 40},
}


from typing import Annotated
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()

# 🧱 Define the item structure (Pydantic model)
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# 🚀 Route: PUT to update item
@app.put("/items/{item_id}")
async def update_item(
    # 1️⃣ Path Parameter with constraints
    item_id: Annotated[int, Path(title="The ID of the item", ge=0, le=1000)],

    # 2️⃣ Optional Query Parameter
    q: str | None = None,

    # 3️⃣ Optional Body Parameter (Item details)
    item: Item | None = None,
):
    results = {"item_id": item_id}

    if q:
        results.update({"query": q})
    if item:
        results.update({"item": item})
    
    return results


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return fake_items_db.get(item_id, {"error": "Item not found"})
