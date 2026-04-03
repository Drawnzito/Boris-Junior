#Este código roda no seu PC com a VPN ligada.

import os
from fastapi import FastAPI
from hdbcli import dbapi
from dotenv import load_dotenv

# Carrega as senhas do arquivo .env
load_dotenv()

app = FastAPI()

def conectar_sap():
    return dbapi.connect(
        address=os.getenv("SAP_HOST"),
        port=30015, # Verifique se a porta do seu HANA é esta
        user=os.getenv("SAP_USER"),
        password=os.getenv("SAP_PASS")
    )

@app.get("/cliente/{medidor}")
def buscar_cliente(medidor: str):
    try:
        conn = conectar_sap()
        cursor = conn.cursor()
        
        # Na api_interna.py, dentro da função buscar_cliente:
        query = f'SELECT * FROM "CLP124051"."PLANILHAO_CLIENTE" WHERE ZCGINSTAL = \'{medidor}\''
        
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return {"status": "sucesso", "data": result}
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}