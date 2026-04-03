# api_externa/main.py

from fastapi import FastAPI, HTTPException
import requests
import jwt
from asyncio import Semaphore

import os
# Ele vai tentar ler do Render, se não achar, usa o localhost (para teste)
API_INTERNA_URL = os.getenv("API_INTERNA_URL", "http://localhost:8000")
SECRET = os.getenv("SECRET_JWT", "chave-secreta-temporaria")

app = FastAPI()

SECRET = "segredo_jwt"
semaforo = Semaphore(20)

#API_INTERNA_URL = "http://SEU_IP_LOCAL:8000"

def verificar_token(token):
    try:
        return jwt.decode(token, SECRET, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.get("/dados/{medidor}")
async def get_dados(medidor: str, token: str):
    verificar_token(token)

    async with semaforo:
        try:
            response = requests.get(f"{API_INTERNA_URL}/cliente/{medidor}")
            return response.json()
        except:
            raise HTTPException(status_code=500, detail="Erro na API interna")