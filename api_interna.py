# api_interna/main.py

from fastapi import FastAPI
from hdbcli import dbapi
import os
from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("SAP_HOST")

app = FastAPI()

def conectar_sap():
    return dbapi.connect(
        address=os.getenv("SAP_HOST"),
        port=30015,
        user=os.getenv("SAP_USER"),
        password=os.getenv("SAP_PASS")
    )

@app.get("/cliente/{medidor}")
def buscar_cliente(medidor: str):
    conn = conectar_sap()
    cursor = conn.cursor()

    query = f"""
        SELECT * 
        FROM tabela_clientes
        WHERE medidor = '{medidor}'
    """

    cursor.execute(query)
    result = cursor.fetchall()

    return {"data": result}