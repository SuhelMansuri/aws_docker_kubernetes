from typing import Union

from fastapi import FastAPI     # functionality for API is provided by the FastAPI Python class.
import pandas as pd

app = FastAPI()                 # creates a FastAPI instance


@app.get("/")                   # python decorator that specifies to FastAPI
#async def root():
def read_root():
    return{"API that returns" : "Shifts from a database"}

#@app.get("/shifts/{shift_id}")                   
#def read_shift(shift_id: int):
#    return {"shift_id": shift_id}

@app.get("/shifts")                   
def shift_data():
    df = pd.read_csv("/code/app/shift_data.csv").T.to_dict()
    return df