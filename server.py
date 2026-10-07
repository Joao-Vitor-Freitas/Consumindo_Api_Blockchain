from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

BASE_URL = "https://api.blockchain.info/explorer-gateway-kt"

@app.get("/whales")
def get_whales(limit: int = 5):
    try:
        res_blocks = requests.post(f"{BASE_URL}/btc/blocks", json={"limit": 1}, verify=False, timeout=10)
        res_blocks.raise_for_status()
        
        blocks_data = res_blocks.json().get("blocks", [])
        if not blocks_data:
            raise HTTPException(status_code=404, detail="No blocks found from API.")
            
        bloco_hash = blocks_data[0]["hash"]
        
        res_block = requests.post(f"{BASE_URL}/btc/block", json={"hash": bloco_hash}, verify=False, timeout=10)
        res_block.raise_for_status()
        
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
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Erro de comunicação com a API externa: {str(e)}")
    except (KeyError, IndexError) as e:
        raise HTTPException(status_code=500, detail=f"Erro ao estruturar os dados da API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado: {str(e)}")