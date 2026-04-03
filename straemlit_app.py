# streamlit_app/app.py

import streamlit as st
import requests
import os
# O Streamlit precisa saber onde a API Externa (FastAPI) está rodando
API_URL = os.getenv("API_EXTERNA_URL")

st.title("Consulta de Cliente")

# LOGIN
if "token" not in st.session_state:
    user = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        res = requests.post(f"{API_URL}/login", params={
            "username": user,
            "password": password
        })
        
        if res.status_code == 200:
            st.session_state["token"] = res.json()["token"]
        else:
            st.error("Erro no login")

# CONSULTA
if "token" in st.session_state:
    medidor = st.text_input("Digite o medidor")

    @st.cache_data(ttl=300)
    def buscar_dados(medidor):
        res = requests.get(
            f"{API_URL}/dados/{medidor}",
            params={"token": st.session_state["token"]}
        )
        return res.json()

    if st.button("Buscar"):
        dados = buscar_dados(medidor)
        st.write(dados)