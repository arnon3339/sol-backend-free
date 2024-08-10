from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.transaction import Transaction

import asyncio

async def run(endpoint, mint_address):
    async with AsyncClient(endpoint) as client:
        res = await client.is_connected()
        nft_signaters = await client.get_signatures_for_address(
                Pubkey.from_string(mint_address),
                commitment="finalized",
                limit=5
                )
        print(nft_signaters)

asyncio.run(run(
    "https://api.devnet.solana.com",
    "ETgXpgGJcZMticwaJeahMpapJqncRJ1Ro9SVdNRsGz9e"
))