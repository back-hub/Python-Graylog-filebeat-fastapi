import sys
import logging
from fastapi import FastAPI, HTTPException
from typing import Optional
from pydantic import BaseModel

_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"

def get_file_handler():
    file_handler = logging.FileHandler("./logs/file.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_log_format))
    return file_handler

def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(_log_format))
    return stream_handler

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger

logger = get_logger(__name__)


db = {}

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@app.get("/items/{item_name}")
async def read_item(item_name: str):
    logger.info(f"[Reading an item] - {item_name}")
    item = db.get(item_name)
    if not item:
        logger.error(f"[Item not found] - {item_name}")
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/items/")
async def create_item(item: Item):
    logger.info(f"[Creating an item] - {item.name}")
    if item.name in db:
        logger.error(f"[Item already exist] - {item.name}")
        raise HTTPException(
            status_code=403, detail="Item already exist"
        )
    item_dict = item.dict()
    if item.tax:
        logger.info(f"[Calculating price with tax] - tax: {item.tax}")
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    db[item.name] = item
    return item_dict