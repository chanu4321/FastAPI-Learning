from fastapi import FastAPI, Query, HTTPException
from models import MenuItem, MenuResponse
from data import menu_items

app = FastAPI(
    title="Chai Point Menu API",
    description=(
        "Read-only menu API for Kiosk displays and mobile app"
    )
)

@app.get("/")
def root():
    return {"message" : "Welcome to Chai point menu API"}

@app.get("/menu", response_model=MenuResponse)
def get_menu(category: str | None = Query(None, description="Filter by chai, snack or combo")):
    if category:
        filtered = [item for item in menu_items if item["category"] == category.lower()]
        if not filtered:
            raise HTTPException(status_code=404, detail=f"Noitem found in category: {category}")
        return MenuResponse(count=len(filtered), items=filtered)

    return MenuResponse(count=len(menu_items), items=menu_items)

@app.get("/menu/{id}", response_model=MenuItem)
def get_item(id: int):
    for item in menu_items:
        if item["id"] == id:
            return item
    raise HTTPException(status_code=404, detail=f"Menu item with id {id} not found")
