from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/items/")
def read_root():
    return {"Id": "Teste", "Name": "Teste", "Price": 0.0, "is_offer": False}

@app.get("/items/{item_id}")
def read_item(item_id: str, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: str, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.post("/items")
def insert_item(item_id: str, item: Item):
    return {"item_name": item.name, "item_id": item_id}