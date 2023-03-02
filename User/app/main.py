from typing import Union

from fastapi import FastAPI     # functionality for API is provided by the FastAPI Python class.
import pandas as pd

app = FastAPI()                 # creates a FastAPI instance


@app.get("/")                   # python decorator that specifies to FastAPI
#async def root():
def read_root():
    return{"API that returns" : "Users from a database"}

#@app.get("/users/{user_id}")                   
#def read_user(user_id: int):
#    return {"user_id": user_id}

@app.get("/users")                   
def user_data():
    df = pd.read_csv("/code/app/user_data.csv").T.to_dict()
    return df