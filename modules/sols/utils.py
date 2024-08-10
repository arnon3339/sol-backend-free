from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.transaction import Transaction
import json

async def get_monkey_owners(endpoint: str, mint_address: str):
    nft_owners = []
    async with AsyncClient(endpoint) as client:
        res = await client.is_connected()
        nft_signaters = []
        while True:
            try:
                nft_signaters = await client.get_signatures_for_address(
                        Pubkey.from_string(mint_address),
                        commitment="finalized"
                        )
                break
            except:
                continue
        nft_data_json = json.loads(nft_signaters.to_json())
        signatures = [d["signature"] for d in nft_data_json['result']]
        for signature in signatures:
            print(signature)
            found_new_owner = False
            tx = await client.get_transaction(Signature.from_string(signature), commitment="finalized", max_supported_transaction_version=3)
            tx_json_data =json.loads(tx.to_json())
            for lgm in tx_json_data['result']['meta']['logMessages']:
                if found_new_owner:
                    break
                elif "TransferChecked" in lgm:
                    accounts = tx_json_data['result']['meta']['postTokenBalances']
                    for acc in accounts:
                        if int(acc['uiTokenAmount']['amount']) > 0:
                            found_new_owner = True
                            nft_owners.append(acc['owner'])
    return nft_owners

def get_hidden_key(key):
    return key[:8] + "*"*(len(key) - 16) + key[-8:]
