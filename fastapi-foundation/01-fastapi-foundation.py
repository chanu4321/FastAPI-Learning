from fastapi import FastAPI
from fastapi import Request
# import uvicorn

app = FastAPI(
    title="Swiggy Order Delivery Service",
    description=(
        "Internal API for managing orders"
        " Handle creation, tracking of delivery systems"
    ),
    version="1.2.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)                               # config for documentation

@app.get("/")
def read_root():
    """Root endpoint - Health Check"""
    # FastAPI converts this dict into JSON
    return {"message": "Welcome to Swiggy Order Service", "status" : "healthy"}


@app.get("/about")
def about():
    """Returns API metadata"""
    return {
        "service" : "order-service",
        "team" : "backend platform",
        "region" : "ap-south-1",
        "version" : "1.2.2"
    }

@app.get("/orders")
def list_orders() -> dict[str, list[dict[str, str|int]]]:
    """List recent orders"""
    return {
        "orders": [
            {"id":1, "item":"Butter Paneer", "status":"Delivered"},
            {"id":2, "item":"Masala Dosa", "status":"Preparing"},
            {"id":3, "item":"Chicken Tikka", "status":"Delivered"}
        ]
    }

@app.get("/orders/status")
def order_status() -> dict[str, str|int]:
    """Get Order Status"""
    return {
        "total_today" : 2_340,
        "top_city" : "Bengaluru"
    }

@app.get("/debug/request-info")
async def request_info(request: Request) -> dict[str, str | dict[str, str] ]:
    """Inspect the Raw Request object"""
    return {
        "method": request.method,
        "url": str(request.url),
        "headers" : dict(request.headers),
        "path_params" : request.path_params,
        "query_params" : dict(request.query_params)
    }


@app.get(
    "/orders/active",
    summary="Get Active Orders",
    description=(
        "Returns all orders that are currently being prepared"
        " or are out for delivery"
    ),
    tags=["orders"],  #category to group the requests
    response_description="List of active order objects",
    deprecated=False
)
def get_active_order() -> dict[str, list[dict[str,int|str]]]:
    """This docstring also appears in docs"""
    return {
        "active_orders": [
            {"id": 1, "item": "Masala Dosa", "status": "out_for_delivery"}
        ]
    }


@app.get("/restaurants", tags=["restaurants"])
def list_restro():
    """another docstring for another endpoint"""
    return {
        "retaurants" : [
            {"test" : "test"} 
        ]
    }

@app.get("/restaurants/delhi", tags=["restaurants"])
def list_restro_delhi():
    """another docstring for another endpoint"""
    return {
        "retaurants" : [
            {"test" : "test"} 
        ]
    }