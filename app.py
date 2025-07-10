# app.py
import streamlit as st
from api import get_matches
import pandas as pd

st.title("BetInsight - Estatísticas de Apostas")

competicao = st.selectbox("Escolha a competição", ["PL", "SA", "BL1", "PD", "FL1"])
temporada = st.text_input("Temporada", "2024")

if st.button("Buscar partidas"):
    partidas = get_matches(competicao, temporada)
    if partidas:
        df = pd.DataFrame([{
            "Data": m["utcDate"],
            "Casa": m["homeTeam"]["name"],
            "Visitante": m["awayTeam"]["name"],
            "Status": m["status"]
        } for m in partidas])
        st.dataframe(df)
    else:
        st.warning("Nenhuma partida encontrada.")