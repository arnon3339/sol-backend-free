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
import re

async_session = None
sonala_endpoint = None

@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    global async_session, sonala_endpoint
    engine = None
    config = dotenv_values("../.env.local")
    if config["ENV"] == "PRODUCTION":
        engine = create_async_engine(config["POSTGRES_PROD"])
        sonala_endpoint = config["SOLANA_ENDPOINT"]
    else:
        sonala_endpoint = config["SOLANA_ENDPOINT"]
        engine = create_async_engine(config["POSTGRES_DEV"])
    async with engine.begin() as conn:
        pass
        await conn.run_sync(NftBase.metadata.create_all)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    yield
    await engine.dispose()


origins = [
    "http://localhost:3000",
    "https://localhost:3000",
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
    global async_session
    try:
        result = await crudcard.get_all_cards(async_session) 
        return result
    except:
        raise HTTPException(status_code=500, detail="Server error!")
    return []

@app.get("/api/limited-cards")
async def get_limited_cards(model: QueryCard = Depends()) -> Optional[Cards]:
    global async_session
    #try:
    result = await crudcard.get_limited_cards(async_session, model, model.page) 
    return result
    #except:
        #raise HTTPException(status_code=500, detail="Server error!")
    return None

@app.get("/api/imgshow")
async def get_imgshow_by_name(monkey_show: MonkeyShow = Depends()) -> MonkeyShowData:
    global async_session, sonala_endpoint
    result = await imgshow.get_imgshow(async_session, sonala_endpoint, monkey_show)
    return result

@app.get("/api/nftowners")
async def get_owners_by_mint(name: str, mint: bool, kind: str) -> List[Optional[str]]:
    global async_session, sonala_endpoint
    owners = []
    if not mint:
        return owners
    else:
        owners = await imgshow.get_nft_owners(async_session, sonala_endpoint, name, kind)
        return owners
    return []

@app.get("/api/imgblur")
def get_blured_image(img_names: str) -> List[Imgb64]:
    imgb64_list = [Imgb64(name=img_name, b64code=img2b64blur(img_name)) for img_name in img_names.split(' ')]
    return imgb64_list 
