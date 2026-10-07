import streamlit as st
import requests

st.title("Bitcoin Whale Tracker")

if st.button("Buscar Maiores Transações"):
    try:
        response = requests.get("http://127.0.0.1:8000/whales?limit=5")
        
        if response.status_code == 200:
            data = response.json()
            st.write(f"**Bloco analisado:** {data['bloco']}")
            st.dataframe(data["whales"])
        else:
            st.error("Erro ao buscar dados na API.")
            
    except Exception:
        st.error("Certifique-se de que o FastAPI está rodando (`uvicorn main:app --reload`).")