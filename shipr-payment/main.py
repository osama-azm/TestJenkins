from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel, NotFoundError
from starlette.requests import Request
from dotenv import load_dotenv
import requests
import time
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

class Order(HashModel):
    product_id: str
    quantity: int
    price: float
    fee: float
    total: float
    status: str

    class Meta:
        database = redis
        model_key_prefix = "order"

def format_order(pk: str):
    order = Order.get(pk)
    return {
        "id": order.pk,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "price": order.price,
        "fee": order.fee,
        "total": order.total,
        "status": order.status
    }

@app.get("/orders")
def get_all_orders():
    return [format_order(pk) for pk in Order.all_pks()]

@app.get("/orders/{pk}")
def get_order(pk: str):
    try:
        return Order.get(pk)
    except NotFoundError:
        raise HTTPException(status_code=404, detail=f"Order with pk {pk} not found")

@app.post("/orders")
async def create_order(request: Request, background_tasks: BackgroundTasks):
    data = await request.json()

    product_service_url = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8000")
    req = requests.get(f"{product_service_url}/products/" + data["id"])
    product = req.json()

    fee_percentage = float(os.getenv("FEE_PERCENTAGE", 0.2))
    fee = fee_percentage * product["price"]
    total = (1 + fee_percentage) * product["price"]

    order = Order(
        product_id=data["id"],
        quantity=data["quantity"],
        price=product["price"],
        fee=fee,
        total=total,
        status="pending"
    )

    order.save()

    background_tasks.add_task(order_completed, order)
    
    return order

def order_completed(order: Order):
    time.sleep(5)
    order.status = "completed"
    order.save()
    redis.xadd("order_completed", order.dict(), '*')
