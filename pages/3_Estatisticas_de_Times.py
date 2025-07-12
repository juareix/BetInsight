import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from api import get_teams_by_competition, get_last_matches_by_team
#################################################################
####### Modulo de busca de estatistica de times #########

st.subheader("📊 Estatísticas de Times (últimos jogos)")

competicao_estat = st.selectbox("Selecione a competição", ["PL", "SA", "BL1", "PD", "FL1"], key="estat")

if st.button("Buscar times"):
    times = get_teams_by_competition(competicao_estat)
    nome_times = [t["name"] for t in times]
    time_selecionado = st.selectbox("Escolha o time", nome_times)

    team_info = next((t for t in times if t["name"] == time_selecionado), None)

    temporadas_disponiveis = ["2024", "2023", "2022", "2021"]
    temporada_selecionada = st.selectbox("Temporada", temporadas_disponiveis, index=0)


    if team_info:
        partidas = get_last_matches_by_team(team_info["id"], season=temporada_selecionada)
        if partidas:
            df_partidas = pd.DataFrame([{
                "Data": m["utcDate"][:10],
                "Adversário": (
                    m["homeTeam"]["name"] if m["awayTeam"]["id"] == team_info["id"]
                    else m["awayTeam"]["name"]
                ),
                "Local": "Casa" if m["homeTeam"]["id"] == team_info["id"] else "Fora",
                "Placar": f'{m["score"]["fullTime"]["home"]} x {m["score"]["fullTime"]["away"]}',
                "Resultado": (
                    "Ganhou" if (
                        (m["homeTeam"]["id"] == team_info["id"] and m["score"]["winner"] == "HOME_TEAM") or
                        (m["awayTeam"]["id"] == team_info["id"] and m["score"]["winner"] == "AWAY_TEAM")
                    ) else ("Empatou" if m["score"]["winner"] == "DRAW" else "Perdeu")
                )
            } for m in partidas])
            st.dataframe(df_partidas)
        else:
            st.warning("Não foi possível buscar os últimos jogos.")


#################################################################