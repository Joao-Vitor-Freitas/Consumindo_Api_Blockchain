from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    url = "https://api.blockchain.info/explorer-gateway-kt"
    payload_blocks = {
        "limit": 1
    }
    headers = {"Content-Type": "application/json"}
    
    res = requests.post(f"{url}/btc/blocks", json=payload_blocks, headers=headers, verify=False)
    data = res.json()
    hash_bloco = data["blocks"][0]["hash"]
    
    payload_specific_block = {
        "hash": hash_bloco
    }
    response_block = requests.post(f"{url}/btc/block", json=payload_specific_block, headers=headers, verify=False)
    transactions = response_block.json().get("txs", [])

    lista_transacoes_processadas = []

    for tx in transactions:
        valor_total_tx = sum(output.get("value", 0) for output in tx.get("outputs", []))
        
        endereco_destino = None
        for output in tx.get("outputs", []):
            if output.get("address"):
                endereco_destino = output.get("address")
                break

        lista_transacoes_processadas.append({
            "txId": tx.get("txId"),
            "endereco": endereco_destino,
            "valor_satoshis": valor_total_tx,
            "valor_btc": valor_total_tx / 100_000_000 # Convertendo para BTC para ficar legível
        })

    lista_transacoes_processadas.sort(key=lambda x: x["valor_satoshis"], reverse=True)

    return {
        "bloco_analisado": hash_bloco,
        "maiores_transacoes_whales": lista_transacoes_processadas[:5]
    }