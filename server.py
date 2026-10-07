from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

BASE_URL = "https://api.blockchain.info/explorer-gateway-kt"

@app.get("/whales")
def get_whales(limit: int = 5):
    try:
        res_blocks = requests.post(f"{BASE_URL}/btc/blocks", json={"limit": 1}, verify=False)
        bloco_hash = res_blocks.json()["blocks"][0]["hash"]
        
        res_block = requests.post(f"{BASE_URL}/btc/block", json={"hash": bloco_hash}, verify=False)
        transactions = res_block.json().get("txs", [])

        lista = []
        for tx in transactions:
            valor_total = sum(out.get("value", 0) for out in tx.get("outputs", []))
            
            endereco = next((out.get("address") for out in tx.get("outputs", []) if out.get("address")), "Desconhecido")

            lista.append({
                "txId": tx.get("txId"),
                "endereco": endereco,
                "valor_btc": valor_total / 100_000_000
            })

        lista.sort(key=lambda x: x["valor_btc"], reverse=True)

        return {
            "bloco": bloco_hash,
            "whales": lista[:limit]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar dados: {str(e)}")