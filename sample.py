from fastapi import FastAPI
from typing import Optional
app = FastAPI()  # am creating an instance of this fastapi 
# this app is the object that will define the diff diff routes ! (get post put delete)



# fake data 


fake_items_db = [
    {"item_name": "Apple", "category": "fruit", "price": 10},
    {"item_name": "Banana", "category": "fruit", "price": 5},
    {"item_name": "Milk", "category": "dairy", "price": 30},
    {"item_name": "Bread", "category": "bakery", "price": 25},
    {"item_name": "Cheese", "category": "dairy", "price": 40},
]






@app.get("/")  # route decorators and this / you see is called as URL 
async def root():                        # async its called as asyncronous fucntion in python means you can send multiple requests effificiently
    return {"message": "Hello World how are you"}
#to run this server we have uvicorn in python 

# path parameters

@app.get("/items/{item_id}")
async def read_item(item_id : int):
    grocery_items = {
        1: "Apple",
        2: "Banana",
        3: "Milk",
        37: "All products"
    } 
    item = grocery_items.get(item_id, "Item not found")
    return {"item_id": item_id, "name": item}


# # Query parameters
# Query parameters are optional key-value pairs added to the end of a URL using ? and &.

# They are used to filter, sort, paginate, or customize data fetching from your API.
#imagine your grocary app has 1000 items 


# Code Part	Meaning
# @app.get("/items/")	Route for /items/
# skip: int = 0	A query parameter. Default value is 0 (skip nothing)
# limit: int = 10	A query parameter. Default is 10 (return up to 10 items)
# fake_items_db[...]	You're slicing the list: db[start:end]

#http://127.0.0.1:8000/items/?skip=1&limit=2




@app.get("/items/")
async def read_items(
    category: Optional[str] = None,
    max_price: Optional[int] = None,
    skip: int = 0,
    limit: int = 10
):
    results = fake_items_db


    # Filter by category
    if category:
        results = [item for item in results if item["category"] == category]

    # Filter by price
    if max_price is not None:
        results = [item for item in results if item["price"] <= max_price]

    # Apply pagination
    return results[skip : skip + limit]



# Try the /items/ endpoint

# Use:

# category = dairy

# max_price = 35

# skip = 0, limit = 10

### request body in endpoints 


# BaseModel is a class provided by Pydantic, 
# which FastAPI uses to validate, parse, and document data sent to your API (especially in POST requests).



from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# Concept	Purpose
# BaseModel	Defines the shape of incoming data
# Pydantic	Library FastAPI uses for validation
# Fields	Defined like name: str, tax: float
# None = None	Makes a field optional
# FastAPI + Model	Automatically checks incoming data



# sample for basemodel

# main.py
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item




#query paraeters with string

from fastapi import FastAPI

app = FastAPI()

@app.get("/items/")
async def read_items(q: str | None = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results




# same with post method 


from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Example database
fake_items_db = [
    {"name": "milk", "price": 30},
    {"name": "bread", "price": 20},
    {"name": "cheese", "price": 70},
]

# Search filter model
class SearchFilters(BaseModel):
    name: Optional[str] = None
    max_price: Optional[float] = None

@app.post("/items/search")
async def search_items(filters: SearchFilters):
    results = fake_items_db

    if filters.name:
        results = [item for item in results if filters.name.lower() in item["name"].lower()]
    
    if filters.max_price is not None:
        results = [item for item in results if item["price"] <= filters.max_price]

    return {"results": results}
