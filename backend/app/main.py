from fastapi import FastAPI

from app.api.routers import organization
from app.api.routers.customer import router as customer_router
from app.api.routers.device import router as device_router
from app.api.routers.diagnostic import router as diagnostic_router
from app.api.routers.material import router as material_router
from app.api.routers.order import router as order_router
from app.api.routers.order_actions import router as order_actions_router
from app.api.routers.order_item import router as order_item_router
from app.api.routers.price_list import router as price_list_router
from app.api.routers.price_list_item import (
    router as price_list_item_router,
)
from app.api.routers.repair import router as repair_router
from app.api.routers.verification import router as verification_router
from app.api.routers.verification_actions import (
    router as verification_actions_router,
)
from app.api.routers.warehouse import router as warehouse_router
from app.api.routers.warehouse_movement import router as warehouse_movement_router
from app.api.routers.warehouse_stock import router as warehouse_stock_router
from app.api.routers.workflow import router as workflow_router

app = FastAPI(title="Sphere")
app.include_router(organization.router)
app.include_router(customer_router)
app.include_router(order_router)
app.include_router(order_actions_router)
app.include_router(order_item_router)
app.include_router(verification_router)
app.include_router(verification_actions_router)
app.include_router(diagnostic_router)
app.include_router(repair_router)
app.include_router(material_router)
app.include_router(warehouse_router)
app.include_router(warehouse_stock_router)
app.include_router(warehouse_movement_router)
app.include_router(price_list_router)
app.include_router(price_list_item_router)
app.include_router(device_router)
app.include_router(workflow_router)


@app.get("/health")
def health():
    return {"status": "ok"}
