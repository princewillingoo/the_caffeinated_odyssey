from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from time import sleep
from collections import deque
import threading
import random

client_app = FastAPI()
barista_app = FastAPI()

order_queue = deque()
order_status = {}
order_event = threading.Event()


class OrderSchema(BaseModel):
    client_name: str
    coffee_type: str

    @field_validator("coffee_type")
    def check_coffee_type(cls, v):
        if v != "americano":
            raise ValueError("Only americano is allowed")
        return v


class FinishOrderSchema(BaseModel):
    order_id: int


@client_app.post("/order/")
async def order_coffee(order: OrderSchema, req: Request):
    client_ip = req.client.host
    # Check for DDoS-like behavior
    if list(order_queue).count(client_ip) > 500:
        raise HTTPException(
            status_code=429,
            detail="Slow down, champ! We can only handle so many americano requests at once!",
        )
    order_id = len(order_queue) + 1
    order_queue.append((order_id, order.client_name, order.coffee_type))
    order_status[order_id] = "queued"

    # Wait for the order to be ready
    while order_status[order_id] != "ready":
        order_event.wait()

    return JSONResponse(
        status_code=200, content={"order_id": order_id, "status": "ready"}
    )


@barista_app.get("/start/")
async def start_order():
    if order_queue:
        order_id, client_name, coffee_type = order_queue.popleft()
        order_status[order_id] = "in_progress"
        return {
            "order_id": order_id,
            "client_name": client_name,
            "coffee_type": coffee_type,
        }
    return JSONResponse(status_code=200, content={"message": "No orders in the queue"})


@barista_app.post("/finish/")
async def finish_order(order: FinishOrderSchema):
    order_id = order.order_id
    if order_id in order_status and order_status[order_id] == "in_progress":
        sleep(random.randint(30, 60))  # Simulate brewing time
        order_status[order_id] = "ready"
        order_event.set()
        return JSONResponse(
            status_code=200, content={"order_id": order_id, "status": "ready"}
        )
    raise HTTPException(status_code=404, detail="Order not found or not in progress")


def run_client_app():
    import uvicorn

    uvicorn.run(client_app, host="0.0.0.0", port=8000)


def run_barista_app():
    import uvicorn

    uvicorn.run(barista_app, host="0.0.0.0", port=8001)


if __name__ == "__main__":
    threading.Thread(target=run_client_app).start()
    threading.Thread(target=run_barista_app).start()
