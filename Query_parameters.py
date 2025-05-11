#Query parameters with string and integers


from typing import Annotated   #this annoted has some extra info , validation, rules, descriptions 
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

@app.get("/items/")
async def read_items(q: Annotated[list[str] | None, Query(max_length=50)] = None):
    return {"queries": q}


@app.get("/items/")
async def read_items(
    q: Annotated[list[str] | None, Query(max_length=20)] = None
):
    return {"queries": q}


# GET /items/?q=milk&limit=
# 
# 
# 5  after question mark if yoy change it is query parameter
# 


# Let’s say you’re running an online grocery store:

# Task	FastAPI Input Type	Example
# Get item with ID 42	Path	/items/42
# Search for items containing "milk"	Query	/items/?q=milk
# Filter items by category and max price	Query	/items/?category=dairy&max_price=50



from typing import Annotated
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
async def read_items(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

#query parameters with more details


from typing import Annotated, Literal
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

# 🎯 Define your query parameters as a model
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)  # max 100 items
    offset: int = Field(0, ge=0)           # start position
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []  # optional filters

# 📦 Use that model as a query param input
@app.get("/items/")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query
