import streamlit as st
import pandas as pd
from api import get_teams_by_competition, get_last_matches_by_team
from utils import partidas_para_df, calcular_medias_gols

st.set_page_config(page_title="⚔️ Comparador de Times", page_icon="⚔️")
st.title("⚔️ Comparador de Times")

# Seleção da competição e temporada
comp = st.selectbox("Competição", ["PL", "PD", "SA", "FL1", "BL1"])
temporada = st.selectbox("Temporada", ["2024", "2023", "2022"])

# Carregar times
times = get_teams_by_competition(comp)
nomes = [t["name"] for t in times]

# Selecionar Time A e Time B
col1, col2 = st.columns(2)
with col1:
    time_a = st.selectbox("Time A", nomes, key="time_a")
with col2:
    time_b = st.selectbox("Time B", nomes, key="time_b")

# Botão de comparação
if st.button("Comparar"):
    def stats_time(nome_time):
        time = next(t for t in times if t["name"] == nome_time)
        partidas = get_last_matches_by_team(time["id"], season=temporada, limit=10)
        
        if not partidas:
            return {"Gols Marcados": 0, "Gols Sofridos": 0, "Vitórias (%)": 0}

        df = partidas_para_df(partidas, time["id"])
        media_pro, media_contra = calcular_medias_gols(df)
        pct_vitorias = (df["Resultado"] == "Vitória").mean() * 100

        return {
            "Gols Marcados": round(media_pro, 2),
            "Gols Sofridos": round(media_contra, 2),
            "Vitórias (%)": round(pct_vitorias, 1)
        }

    st.subheader("📊 Estatísticas Comparativas")
    dados_a = stats_time(time_a)
    dados_b = stats_time(time_b)

    df_cmp = pd.DataFrame([dados_a, dados_b], index=[time_a, time_b])
    st.dataframe(df_cmp)

