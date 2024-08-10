from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from modules.models.dbmodels import NftAtt, NftMint, MintCreator
from modules.models.resmodels import Card, Cards
from modules.models.apimodels import QueryCard
from typing import Optional, List
from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import selectinload, lazyload
import re

from modules.utils import get_att_list, get_found_set, NFT_ATTS

async def get_all_cards(async_session: async_sessionmaker[AsyncSession]) -> List[Optional[Card]]:
    try:
        async with async_session() as session:
            stmt =  select(NftAtt.name, NftAtt.img).order_by(NftAtt.name.asc())
            result = await session.execute(stmt)
        return [Card(name=card[0], img=card[1], kind=0) for card in result.fetchall()]
    except:
        raise Exception("Database error!")
    return []


async def get_limited_cards(async_session: async_sessionmaker[AsyncSession], model: QueryCard,
                                    offset: int = 0, limit: int = 32) -> List[Optional[Card]]:
    count = 0
    is_search = False
    search_list = re.split("\s+", model.search.lower())
    for search in search_list:
        if search != '':
            is_search = True
            break
    ref_att_names = [
        "body",
        "head",
        "eyes",
        "mouth",
        "clothe",
        "eyesacc",
        "mouthacc"
        ]
    filter_atts =\
    {
        "body": get_att_list(model.body, ref_att_names[0]),
        "head": get_att_list(model.head, ref_att_names[1]),
        "eyes": get_att_list(model.eyes, ref_att_names[2]),
        "mouth": get_att_list(model.mouth, ref_att_names[3]),
        "clothe": get_att_list(model.clothe, ref_att_names[4]),
        "eyesacc": get_att_list(model.eyesacc, ref_att_names[5]),
        "mouthacc": get_att_list(model.mouthacc, ref_att_names[6]),
    }
    found_set = {k: set(v) for k, v in NFT_ATTS.items()} if not is_search else \
        {
            "body": get_found_set(model.search.upper(), ref_att_names[0]),
            "head": get_found_set(model.search.upper(), ref_att_names[1]),
            "eyes": get_found_set(model.search.upper(), ref_att_names[2]),
            "mouth": get_found_set(model.search.upper(), ref_att_names[3]),
            "clothe": get_found_set(model.search.upper(), ref_att_names[4]),
            "eyesacc": get_found_set(model.search.upper(), ref_att_names[5]),
            "mouthacc": get_found_set(model.search.upper(), ref_att_names[6]),
        }
    attmint_results = []
    try:
        order = NftAtt.name.asc()
        if model.sort == 1:
            order = NftAtt.name.desc()
        elif model.sort == 2:
            order = NftMint.id.asc()
        elif model.sort == 3:
            order = NftMint.id.desc()
        elif model.sort == 4:
            order = NftAtt.body.asc()
        elif model.sort == 5:
            order = NftAtt.body.desc()
        elif model.sort == 6:
            order = NftAtt.head.asc()
        elif model.sort == 7:
            order = NftAtt.head.desc()
        elif model.sort == 8:
            order = NftAtt.eyes.asc()
        elif model.sort == 9:
            order = NftAtt.eyes.desc()
        elif model.sort == 10:
            order = NftAtt.mouth.asc()
        elif model.sort == 11:
            order = NftAtt.mouth.desc()
        elif model.sort == 12:
            order = NftAtt.clothe.asc()
        elif model.sort == 13:
            order = NftAtt.clothe.desc()
        elif model.sort == 14:
            order = NftAtt.eyesacc.asc()
        elif model.sort == 15:
            order = NftAtt.eyesacc.desc()
        elif model.sort == 16:
            order = NftAtt.mouthacc.asc()
        elif model.sort == 17:
            order = NftAtt.mouthacc.desc()
        async with async_session() as session:
            count_stmt = select(func.count(NftAtt.id))\
                    .filter(
                            and_(
                                and_(
                                    NftAtt.body.in_(filter_atts["body"]),
                                    NftAtt.head.in_(filter_atts["head"]),
                                    NftAtt.eyes.in_(filter_atts["eyes"]),
                                    NftAtt.mouth.in_(filter_atts["mouth"]),
                                    NftAtt.clothe.in_(filter_atts["clothe"]),
                                    NftAtt.eyesacc.in_(filter_atts["eyesacc"]),
                                    NftAtt.mouthacc.in_(filter_atts["mouthacc"])
                                    ),
                                or_(
                                    NftAtt.body.in_(list(found_set["body"])),
                                    NftAtt.head.in_(list(found_set["head"])),
                                    NftAtt.eyes.in_(list(found_set["eyes"])),
                                    NftAtt.mouth.in_(list(found_set["mouth"])),
                                    NftAtt.clothe.in_(list(found_set["clothe"])),
                                    NftAtt.eyesacc.in_(list(found_set["eyesacc"])),
                                    NftAtt.mouthacc.in_(list(found_set["mouthacc"]))
                                    )
                                )
                            )
            count_result = await session.execute(count_stmt)
            count = count_result.scalar()
            stmt = select(NftAtt.name, NftAtt.img, NftAtt.kind, NftAtt.mint)\
                    .filter(
                            and_(
                                and_(
                                    NftAtt.body.in_(filter_atts["body"]),
                                    NftAtt.head.in_(filter_atts["head"]),
                                    NftAtt.eyes.in_(filter_atts["eyes"]),
                                    NftAtt.mouth.in_(filter_atts["mouth"]),
                                    NftAtt.clothe.in_(filter_atts["clothe"]),
                                    NftAtt.eyesacc.in_(filter_atts["eyesacc"]),
                                    NftAtt.mouthacc.in_(filter_atts["mouthacc"])
                                    ),
                                or_(
                                    NftAtt.body.in_(list(found_set["body"])),
                                    NftAtt.head.in_(list(found_set["head"])),
                                    NftAtt.eyes.in_(list(found_set["eyes"])),
                                    NftAtt.mouth.in_(list(found_set["mouth"])),
                                    NftAtt.clothe.in_(list(found_set["clothe"])),
                                    NftAtt.eyesacc.in_(list(found_set["eyesacc"])),
                                    NftAtt.mouthacc.in_(list(found_set["mouthacc"]))
                                    )
                                )
                            )\
                    .outerjoin(NftMint).limit(limit).offset(offset*limit).order_by(order)
            result = await session.execute(stmt)
            result_all = result.all()
            return Cards(count=count, cards=[Card(name=card[0], img=card[1], kind=card[2], 
                                                  mint=True if card[3] else False) for card in result_all])
    except:
        raise Exception("Database error!")
    return None
