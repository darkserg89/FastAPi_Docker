from fastapi import FastAPI
from datetime import datetime
from app.modules import pldap
import os
from dotenv import load_dotenv
import uvicorn

app = FastAPI()
@app.get("/")
async def root():
    return {"greeting":"Hello world"}

@app.get("/date")
async def root():
    return {"current date":str(datetime.now())}

@app.get('/users')
async def ad_users():
    load_dotenv()
    AD_SERVER = os.getenv('AD_SERVER')
    AD_SEARCH_BASE = os.getenv('AD_SEARCH_BASE')
    AD_USER = os.getenv('AD_USER')
    AD_PASSWORD = os.getenv("AD_PASSWORD")
    filter_all_users = os.getenv('filter_all_users')
    attr = os.getenv('attr')
    ldap_query = pldap(AD_SERVER, AD_USER, AD_PASSWORD, AD_SEARCH_BASE, filter_all_users)
    if ldap_query.load():
        result = ldap_query.json_data
        return result
    else:
        result = {'entries': 'error'}
        return result

if __name__ == "__main__":
    uvicorn.run(app,host='127.0.0.1',port=5000)