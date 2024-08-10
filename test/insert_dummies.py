import sys
sys.path.append('../')
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from sqlalchemy import insert 
from dotenv import dotenv_values 
from modules.models.dbmodels import NftAtt, NftMint, MintCreator, NftBase
from typing import List
import asyncio
import tracemalloc
import random
import datetime
import json

def get_atts():
    with open('../data/att_data_final.json') as f:
        data = json.load(f)
    data_out = {}
    for k, v in data.items():
        data_out[k] = v['att']
    return data_out

async def insert_nftatts(async_session, num: int = 200):
    data = []
    data_atts = get_atts()
    uris = [
             "https://arweave.net/Uu67k0VnJNLHZj9q-alyp7yMMvq3tN1kuYC1Q__owE8",
             "https://arweave.net/pGNQwsVi6tnfS3dJEuTNaNaMMd-qeCg_KIMoFwIojng",
             "https://arweave.net/jLNOturufECyFhiznAoLJN5nu_07Q-rTMRpYV1kpM04",
             "https://arweave.net/P1atqsa_up6pQVKpRA5g41Wi8ayZr3sQx__iY64Mmh4",
             "https://arweave.net/HnM4fL56CiAPRb4dblApcwZaw_gvr84QdDkezVfwR_k",
             "https://arweave.net/VV20zuRMyEqaBTTRiAlIT6sDfV5PHNlzAhkHnezgBeU",
             "https://arweave.net/nIMRQBfX_VCE7_iSolv3WAtE9l7_uS27HUjHQ0RO3Hc",
             "https://arweave.net/qIfBSxWTgCsIXLQ6Dcl4hlXfAOvTa9QVAbqJFDx-r3Q",
             "https://arweave.net/zTJv7Fu4OzTxDZbEdbQK3nchhG2zadjdNEmG_h00gmI",
             "https://arweave.net/bGwf_iZGHPf-p2iDs2u8CaimFYe7e7cHMBAJRV3ofKw"
            ]
    imgs = [
            "https://arweave.net/U6TVTr7hyuXeN2fhCMOWh_x_2LiAIrJiSAJIWgLuVwA?ext=png",
            "https://arweave.net/E4Qhd30VOnSqATb-1A5nyl-NRgOwNiRRdWxncBMelI0?ext=png",
            "https://arweave.net/HEC2i89A8GKQy0XTpHCZI2JDDAwhXTtRLwDHULsjdcE?ext=png",
            "https://arweave.net/_SCqSLNVz761elGxPi59G7xz_e4ZjtCKW--oT9lLSCY?ext=png",
            "https://arweave.net/_xBqWbzCPi39dR3XNEED4otZoxSEZTLo-81siV8Dq5c?ext=png",
            "https://arweave.net/zYbuH_fBFiufLX1wIvdKHn8Fx4y58DnjIOEURsb7qcE?ext=png",
            "https://arweave.net/hmN8j2ON6-khEOIru-sJoSKdBDSyx8uFQOyrybOuULs?ext=png",
            "https://arweave.net/e5W75HhN6xgjtzVvh43o4U8m5tXmQBcDKRsfT94QI_U?ext=png",
            "https://arweave.net/Qfh-OPmWg6qzVu0XwdlwoLZuSh_gRJ4H7V8JsKlWhlk?ext=png",
            "https://arweave.net/zr75s2rDUCtPSoX17QnP9_FcL7C43BByeO02byYHkTY?ext=png"
            ]
    for i in range(num):
    # for i in range(len(uris)):
        single_data = {}
        # single_data["name"] = "x" + "0"*(4 - len(str(i))) + str(i)
        single_data["name"] = "0"*(4 - len(str(i))) + str(i)
        single_data["uri"] = random.choice(uris) + str(i)
        single_data["img"] = random.choice(imgs)
        # single_data["uri"] = uris[i]
        # single_data["img"] = imgs[i]
        single_data["kind"] = f"0"
        single_data["body"] = f"BODY-{random.randint(1, 3)}"
        single_data["head"] =  random.choice(data_atts['AccHead'])
        single_data["eyes"] = random.choice(data_atts['Eyes'])
        single_data["mouth"] = random.choice(data_atts['Mouth'])
        single_data["clothe"] = random.choice(data_atts['Clothes'])
        single_data["eyesacc"] = random.choice(data_atts['AccEyes'])
        single_data["mouthacc"] = random.choice(data_atts['AccMouth'])
        single_data["lastupdate"] = datetime.datetime.now()
        data.append(single_data)
    async with async_session() as session:
        stmt = insert(NftAtt).returning(NftAtt.id)
        result = await session.execute(stmt, data)
        await session.commit()

async def main(config):
    tracemalloc.start()
    engine = create_async_engine(config["POSTGRES_DEV"], pool_size=20, max_overflow=0)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(NftBase.metadata.create_all)
    await insert_nftatts(async_session, 1000)
    await engine.dispose()
    tracemalloc.stop()

if __name__ == "__main__":
    config = dotenv_values("../../.env.local")
    asyncio.run(main(config))
