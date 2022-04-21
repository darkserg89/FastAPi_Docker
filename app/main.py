from fastapi import FastAPI
from datetime import datetime
app = FastAPI()
@app.get("/")
async def root():
    return {"greeting":"Hello world"}

@app.get("/date")
async def root():
    return {"current date":str(datetime.now())}