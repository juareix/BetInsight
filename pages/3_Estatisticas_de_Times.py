import streamlit as st
import pandas as pd
from api import get_teams_by_competition, get_last_matches_by_team
from utils import partidas_para_df, calcular_medias_gols

st.set_page_config(page_title="📈 Estatísticas de Times", page_icon="📊")
st.title("📈 Estatísticas de Times")

# Seleção da competição
comp = st.selectbox("Selecione a competição", ["PL", "PD", "SA", "FL1", "BL1"])  # Premier, La Liga, Série A...

# Carrega times da competição
times = get_teams_by_competition(comp)
nomes = [t["name"] for t in times]
time_escolhido = st.selectbox("Escolha o time", nomes)

# Seleção de temporada
temporadas = ["2024", "2023", "2022"]
temporada = st.selectbox("Temporada", temporadas)

# Botão para buscar estatísticas
if st.button("Buscar estatísticas"):
    time = next(t for t in times if t["name"] == time_escolhido)
    partidas = get_last_matches_by_team(time["id"], season=temporada, limit=10)
    
    if not partidas:
        st.warning("Nenhuma partida encontrada para esse time nessa temporada.")
    else:
        df = partidas_para_df(partidas, time["id"])
        media_pro, media_contra = calcular_medias_gols(df)

        st.metric("⚽ Média de Gols Marcados", f"{media_pro:.2f}")
        st.metric("🥅 Média de Gols Sofridos", f"{media_contra:.2f}")

        st.dataframe(df)
