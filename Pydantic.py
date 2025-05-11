
from typing import Annotated, Literal
from fastapi import FastAPI, Path, Query, Body
from pydantic import BaseModel, Field

app = FastAPI()

# 1. Basic Pydantic model for request body
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

# 2. Query Parameters Example (optional with validation)
@app.get("/query-example/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# 3. Path Parameter with validation + Query Param with alias
@app.get("/items/{item_id}")
async def read_item_with_path_query(
    item_id: Annotated[int, Path(title="The ID of the item to get")],
    q: Annotated[str | None, Query(alias="item-query")] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results

# 4. Query Parameter as a Model
class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []

@app.get("/filtered-items/")
async def read_filtered_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

# 5. Mixing Path, Query, Body Model
@app.put("/items/{item_id}")
async def update_item_combined(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)],
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results

# 6. Multiple body models
@app.put("/items/{item_id}/user-update")
async def update_item_user(item_id: int, item: Item, user: User):
    return {"item_id": item_id, "item": item, "user": user}

# 7. Singular body value with Body()
@app.put("/items/{item_id}/importance")
async def update_item_importance(
    *,
    item_id: int,
    item: Item,
    user: User,
    importance: Annotated[int, Body(gt=0)],
    q: str | None = None,
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results
