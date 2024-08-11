from fastapi import FastAPI, HTTPException
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from contextlib import asynccontextmanager
from dotenv import dotenv_values 
from typing import List, Union, Optional, Dict
from modules.models.apimodels import QueryCard, MonkeyShow
from modules.models.resmodels import Cards, Card, Imgb64, MonkeyShowData
from modules.models.dbmodels import NftBase 
from modules.utils import img2b64blur
from modules.crud import crudcard, imgshow
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings
import re
import os

async_session = None

class Settings(BaseSettings):
    
    postgres_prod: str
    postgres_dev: str
    collectionkey: str
    candy_program_id: str
    candy_guard_id: str
    candy_mint_acc: str
    mintsignature: str
    frontend_url: str
    sol_endpoint: str
    
    class Config:
        if os.getenv("ENV") == "production":
            env_file = None  # Use system env variables
        else:
            env_file = ".env"  # Use .env file for development
            
settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global async_session
    engine = None
    if os.getenv("ENV")== "production":
        engine = create_async_engine(settings.postgres_prod)
    else:
        engine = create_async_engine(settings.postgres_dev)
    async with engine.begin() as conn:
        await conn.run_sync(NftBase.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    yield
    await engine.dispose()


origins = [
    settings.frontend_url
]
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

@app.get("/api")
def hello_all():
    return {"message": "Hello All"}


@app.get("/api/cards")
async def get_cards(model: QueryCard = Depends()) -> List[Optional[Card]]:
    try:
        result = await crudcard.get_all_cards(async_session) 
        return result
    except:
        raise HTTPException(status_code=500, detail="Server error!")
    return []

@app.get("/api/limited-cards")
async def get_limited_cards(model: QueryCard = Depends()) -> Optional[Cards]:
    #try:
    result = await crudcard.get_limited_cards(async_session, model, model.page) 
    return result
    #except:
        #raise HTTPException(status_code=500, detail="Server error!")
    return None

@app.get("/api/imgshow")
async def get_imgshow_by_name(monkey_show: MonkeyShow = Depends()) -> MonkeyShowData:
    result = await imgshow.get_imgshow(async_session, settings.sonala_endpoint, monkey_show)
    return result

@app.get("/api/nftowners")
async def get_owners_by_mint(name: str, mint: bool, kind: str) -> List[Optional[str]]:
    owners = []
    if not mint:
        return owners
    else:
        owners = await imgshow.get_nft_owners(async_session, settings.sonala_endpoint, name, kind)
        return owners
    return []

@app.get("/api/imgblur")
def get_blured_image(img_names: str) -> List[Imgb64]:
    imgb64_list = [Imgb64(name=img_name, b64code=img2b64blur(img_name)) for img_name in img_names.split(' ')]
    return imgb64_list 
