from pydantic import BaseModel

# for each module a model is used
# basically validating the response is same as the schema below
class MenuItem(BaseModel):
    id: int
    name: str
    category: str
    price: float
    description: str
    available: bool


class MenuResponse(BaseModel):
    status: str = "success"
    count: int
    items: list[MenuItem]