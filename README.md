# Bitcoin Whale Tracker

## Problema
Muitas pessoas se sentem perdidas em quando investir em criptomoedas e entender para onde o mercado está indo.

## Solução
Buscar as maiores transações ("whales") dentro do bloco mais recente da rede Bitcoin para ter uma ideia clara do volume financeiro que está sendo movimentado no momento e quais carteiras/entidades estão por trás dessas grandes operações.

---

# Como Rodar
Instalar as dependencias:
pip install -r requirements.txt

# Rodar a API:
uvicorn server:app --reload

# Documentacao Swagger:
Acesse http://127.0.0.1:8000/docs no seu navegador.

# Rodar o Streamlit (em outro terminal):
streamlit run app.py