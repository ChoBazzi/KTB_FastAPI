'''
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

df = pd.read_csv('./data/data.csv')

class Item(BaseModel):
    name : str
    price : float

@app.get("/")
async def root():
    return df.to_dict()

@app.get("/items/{item_id}")
async def read_item( item_id : int, q : str , limit : int = 10):
    result_df = df[ df['item_id'] == item_id ][q].head(limit)
    return { "result" : result_df.to_list() }

@app.post("/items/{item_id}")
async def save_item( item_id : int, item : Item ):
    df.loc[len(df.index)] = {
        "item_id" : item_id,
        "name" : item.name,
        "price" : item.price
    }
    return { "result" : f"item_id {item_id} is saved" }
'''
from fastapi import FastAPI
import logging
from router.post_router import router as posts_router
from router.user_router import router as user_router

logging.basicConfig(level=logging.INFO)
app = FastAPI()
app.include_router(posts_router)
app.include_router(user_router)
    









