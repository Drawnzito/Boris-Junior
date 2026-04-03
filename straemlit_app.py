#O frontend que o usuário acessa no celular.

import streamlit as st
import requests
import os

# Pega a URL da API Externa que o Render vai gerar
API_URL = st.secrets.get("API_EXTERNA_URL") or os.getenv("API_EXTERNA_URL")

st.set_page_config(page_title="Consulta SAP", layout="centered")
st.title("🔍 Consulta de Medidores")

if "token" not in st.session_state:
    st.subheader("Login")
    user = st.text_input("Usuário")
    pw = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        try:
            res = requests.post(f"{API_URL}/login", json={"username": user, "password": pw})
            if res.status_code == 200:
                st.session_state["token"] = res.json()["token"]
                st.rerun()
            else:
                st.error("Login inválido")
        except:
            st.error("Não foi possível conectar à API.")

else:
    if st.sidebar.button("Sair"):
        del st.session_state["token"]
        st.rerun()

    medidor = st.text_input("Digite o número do medidor:")
    
    if st.button("Consultar"):
        if medidor:
            with st.spinner("Buscando no SAP..."):
                try:
                    res = requests.get(
                        f"{API_URL}/dados/{medidor}", 
                        params={"token": st.session_state["token"]}
                    )
                    if res.status_code == 200:
                        st.success("Dados encontrados!")
                        st.write(res.json())
                    else:
                        st.warning(f"Atenção: {res.json().get('detail')}")
                except:
                    st.error("Erro na comunicação com o servidor.")