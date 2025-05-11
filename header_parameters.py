from typing import Annotated
from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/products/")
async def get_products(user_agent: Annotated[str | None, Header()] = None):
    return {
        "message": "Here are your products!",
        "user_agent_received": user_agent
    }



##########################

from typing import Annotated
from fastapi import FastAPI, Header
from pydantic import BaseModel

app = FastAPI()


class CommonHeaders(BaseModel):
    host: str
    save_data: bool  # Indicates if the client prefers minimal data usage (mobile)
    if_modified_since: str | None = None  # For caching
    traceparent: str | None = None       # For distributed tracing
    x_tag: list[str] = []                # For tagging request (e.g., marketing campaigns)


@app.get("/products/")
async def get_products(headers: Annotated[CommonHeaders, Header()]):
    return {
        "message": "Products fetched successfully",
        "received_headers": headers
    }



################ return values 

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Define a reusable data model
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

# POST: Create and return a single item
@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Item:
    return item

# GET: Return a list of items
@app.get("/items/", response_model=list[Item])
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0, tags=["sci-fi", "weapon"]),
        Item(name="Plumbus", price=32.0, tags=["home", "weird"]),
    ]
