import streamlit as st
from api import get_teams_by_competition, get_last_matches_by_team
from utils import partidas_para_df, detectar_tendencias

st.set_page_config(page_title="📉 Tendências e Padrões", page_icon="🚨")
st.title("📉 Tendências de Times")

# Seleção da competição e temporada
comp = st.selectbox("Competição", ["PL", "PD", "SA", "FL1", "BL1"])
temporada = st.selectbox("Temporada", ["2024", "2023", "2022"])

# Carregar times
times = get_teams_by_competition(comp)
nomes = [t["name"] for t in times]
time_escolhido = st.selectbox("Escolha o time", nomes)

# Botão de busca
if st.button("Analisar Tendências"):
    time = next(t for t in times if t["name"] == time_escolhido)
    partidas = get_last_matches_by_team(time["id"], season=temporada, limit=10)

    if not partidas:
        st.warning("Nenhuma partida encontrada para esse time nessa temporada.")
    else:
        df = partidas_para_df(partidas, time["id"])
        st.dataframe(df)

        st.subheader("🔍 Tendências Detectadas")
        tendencias = detectar_tendencias(df)

        if tendencias:
            for t in tendencias:
                st.markdown(f"- {t}")
        else:
            st.info("Nenhuma tendência relevante detectada.")
