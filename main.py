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

# Root route
@app.get("/")
async def root():
    return {"message": "Hello World how are you"}

# Path parameter
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    grocery_items = {
        1: "Apple",
        2: "Banana",
        3: "Milk",
        37: "All products"
    }
    item = grocery_items.get(item_id, "Item not found")
    return {"item_id": item_id, "name": item}

# Query parameters
@app.get("/items/")
async def read_items(
    category: Optional[str] = None,
    max_price: Optional[int] = None,
    skip: int = 0,
    limit: int = 10
):
    results = fake_items_db
    if category:
        results = [item for item in results if item["category"] == category]
    if max_price is not None:
        results = [item for item in results if item["price"] <= max_price]
    return results[skip: skip + limit]

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



from typing import Annotated   #this annoted has some extra info , validation, rules, descriptions 
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# pth and query parater

fake_grocery_db = {
    1: {"name": "Milk", "price": 40},
    2: {"name": "Bread", "price": 25},
    3: {"name": "Eggs", "price": 60},
}

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    item = fake_grocery_db.get(item_id, {"error": "Item not found"})
    if q:
        item["search_term"] = q
    return item
