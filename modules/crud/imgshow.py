from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import text

from modules.models.apimodels import  MonkeyShow
from modules.models.resmodels import MonkeyShowData, Card
from modules.models.dbmodels import NftAtt, NftMint
from modules.models.utilmodels import MonkeyAtt
from modules.sols.utils import get_monkey_owners, get_hidden_key

import random as rnd

async def get_imgshow(async_session:async_sessionmaker[AsyncSession], 
                      solana_endpoint: str,
                      monkey_show: MonkeyShow) -> MonkeyShowData:
    monkey_minter = None
    monkey_att = None
    monkey_recoms = []
    num_recoms = 10
    monkey = None
    async with async_session() as session:
        if monkey_show.mint:
            stmt =  select(NftAtt).filter(NftAtt.name == monkey_show.name).options(selectinload(NftAtt.mint))
            result_query = await session.execute(stmt)
            monkey = result_query.fetchone()[0]
            monkey_minter = monkey.mint.minter
            monkey_att = MonkeyAtt(
                    img=monkey.img,
                    kind=monkey_show.kind,
                    body=monkey.body,
                    head=monkey.head,
                    eyes=monkey.eyes,
                    mouth=monkey.mouth,
                    clothe=monkey.clothe,
                    eyesacc=monkey.eyesacc,
                    mouthacc=monkey.mouthacc
                    )
        else:
            stmt =  select(NftAtt).filter(NftAtt.name == monkey_show.name)
            result_query = await session.execute(stmt)
            monkey = result_query.fetchone()[0]
            monkey_att = MonkeyAtt(
                    img=monkey.img,
                    kind=monkey_show.kind,
                    body=monkey.body,
                    head=monkey.head,
                    eyes=monkey.eyes,
                    mouth=monkey.mouth,
                    clothe=monkey.clothe,
                    eyesacc=monkey.eyesacc,
                    mouthacc=monkey.mouthacc
                    )
        att_ids = set()
        for att_i, (att_k, att_v) in enumerate(monkey_att.dict().items()):
            if att_i < 2:
                continue
            res_ids = None
            if att_v:
                stmt_att_ids = text(f"SELECT id FROM nftatt WHERE {att_k} = :att_value")
                res_ids = await session.execute(stmt_att_ids, {'att_value': att_v})
            else:
                stmt_att_ids = text(f"SELECT id FROM nftatt WHERE {att_k} = NULL")
                res_ids = await session.execute(stmt_att_ids)
            att_ids = att_ids | {att_id[0] for att_id in res_ids.fetchall()}
        ids = rnd.sample(list(att_ids), 10)
        stmt_recoms = select(NftAtt.name, NftAtt.kind, NftAtt.img, NftAtt.mint)\
                .filter(NftAtt.id.in_(ids)).outerjoin(NftMint)
        result_recom_monkeys = await session.execute(stmt_recoms)
        recom_monkeys = result_recom_monkeys.fetchall()
        recom_monkey_cards = [Card(name=m[0], kind=m[1], img=m[2], mint=True if m[3] else False) for m in recom_monkeys]
    result = MonkeyShowData(name=monkey_show.name, mint=monkey_show.mint, 
                            atts=monkey_att, recoms=recom_monkey_cards)
    return result

async def get_nft_owners(async_session:async_sessionmaker[AsyncSession], 
                         solana_endpoint: str, nft_name: str, nft_kind: str):
    async with async_session() as session:
        stmt = select(NftAtt).filter(and_(NftAtt.name == nft_name, NftAtt.kind == nft_kind))\
                .options(selectinload(NftAtt.mint))
        res = await session.execute(stmt)
        result = res.fetchone()
        mint = result[0].mint.mint

        # stmt_minter = select(NftMint.minter).filter(NftMint.mint == mint)
        # res_minter = await session.execute(stmt_minter)
        # result_minter = res_minter.fetchone()
        # minter = result_minter[0]
    monkey_owners = await get_monkey_owners(solana_endpoint, mint)
    print(result[0].mint.minter)
    return [get_hidden_key(mint), get_hidden_key(result[0].mint.minter)] + [get_hidden_key(k) for k in monkey_owners]
