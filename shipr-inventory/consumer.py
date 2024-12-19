from redis_om import get_redis_connection, HashModel
from dotenv import load_dotenv
import os
import time

load_dotenv()

key = "order_completed"
group = "inventory-group"

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

def create_redis_group(key, group):
    try:
        redis.xgroup_create(key, group, mkstream=True)
        print(f"Redis group '{group}' created for key '{key}'")
    except Exception as e:
        print(f"Failed to create Redis group '{group}' for key '{key}': {str(e)}")

def read_from_redis_group(group, key):
    try:
        results = redis.xreadgroup(group, key, {key: ">"}, None)
        
        if results != []:
            for result in results:
                obj = result[1][0][1]

                try:
                    product = Product.get(obj['product_id'])
                    print(product)
                    product.stock -= int(obj['quantity'])
                    product.save()
                    print(f"Order {obj['pk']} completed. Updated stock for product {obj['product_id']} to {product.stock}")
                except Exception as e:
                    print(f"Failed to update product stock: {str(e)}")
                    redis.xadd("refund_order", obj, '*')
                
    except Exception as e:
        print(f"Failed to read from Redis group '{group}' for key '{key}': {str(e)}")

def main():
    print("Inventory consumer started. Waiting for orders to be completed...")
    create_redis_group(key, group)

    while True:
        read_from_redis_group(group, key)
        time.sleep(5)

if __name__ == "__main__":
    main()