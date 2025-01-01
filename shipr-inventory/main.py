from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel, NotFoundError
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOW_ORIGINS", "*").split(","),
    allow_methods=os.getenv("ALLOW_METHODS", "*").split(","),
    allow_headers=os.getenv("ALLOW_HEADERS", "*").split(","),
)

redis = get_redis_connection(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 0)),
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: float
    stock: int

    class Meta:
        database = redis
        model_key_prefix = "product"

def format_product(pk: str):
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }

@app.get("/products")
def get_all_products():
    return [format_product(pk) for pk in Product.all_pks()]

@app.get("/products/{pk}")
def get_product(pk: str):
    try:
        return Product.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail=f"Product with pk {pk} not found")

@app.post("/products")
def create_product(product: Product):
    return product.save()

@app.delete("/products/{pk}")
def delete_product(pk: str):
    try:
        product = Product.get(pk)
        Product.delete(pk)
        return {"message": f"Product with pk {pk} deleted"}
    except NotFoundError:
        raise HTTPException(status_code=404, detail=f"Product with pk {pk} not found")

@app.get("/")
async def root():
    return {"message": "Hello World"}
