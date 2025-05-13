from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

app = FastAPI(title=" Product Catalog API")

# In-memory "database"
products_db = {}

# ------------------------------
# Models
# ------------------------------

class Product(BaseModel):
    id: str
    name: str
    price: float
    description: Optional[str] = None
    image_filename: Optional[str] = None


class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


# ------------------------------
# Endpoints
# ------------------------------

@app.post("/products/", response_model=Product)
async def add_product(product: ProductCreate):
    product_id = str(uuid4())
    new_product = Product(id=product_id, **product.dict())
    products_db[product_id] = new_product
    return new_product


@app.get("/products/", response_model=List[Product])
async def get_all_products():
    return list(products_db.values())


@app.get("/products/{product_id}", response_model=Product)
async def get_product_by_id(product_id: str):
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.post("/products/{product_id}/upload-image/")
async def upload_image(
    product_id: str,
    image: UploadFile = File(...),
):
    product = products_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Simulate saving image
    product.image_filename = image.filename
    return {"message": "Image uploaded", "filename": image.filename}


@app.get("/search/")
async def search_products(name: str):
    results = [
        p for p in products_db.values()
        if name.lower() in p.name.lower()
    ]
    return results
