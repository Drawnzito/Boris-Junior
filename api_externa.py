#Este código roda no Render. Ele recebe o login e faz a ponte com a sua casa.

import os
import jwt
import requests
from fastapi import FastAPI, HTTPException, Depends
from asyncio import Semaphore
from pydantic import BaseModel

app = FastAPI()

# Configurações via Variáveis de Ambiente (Render)
SECRET_JWT = os.getenv("SECRET_JWT", "chave-secreta-muito-segura")
API_INTERNA_URL = os.getenv("API_INTERNA_URL", "http://localhost:8000")
semaforo = Semaphore(20) # Limite de 20 usuários simultâneos

class LoginData(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(data: LoginData):
    # Aqui você define um usuário padrão para teste
    # Depois podemos integrar com uma tabela de usuários
    if data.username == "admin" and data.password == "123456":
        token = jwt.encode({"user": data.username}, SECRET_JWT, algorithm="HS256")
        return {"token": token}
    raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

@app.get("/dados/{medidor}")
async def get_dados(medidor: str, token: str):
    # Valida o Token
    try:
        jwt.decode(token, SECRET_JWT, algorithms=["HS256"])
    except:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

    # Tenta buscar os dados na sua máquina (via ngrok)
    async with semaforo:
        try:
            # Chama a api_interna que está no seu PC
            url = f"{API_INTERNA_URL}/cliente/{medidor}"
            response = requests.get(url, timeout=10)
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao conectar na API interna: {str(e)}")