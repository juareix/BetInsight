# api.py
import requests
import streamlit as st

HEADERS = {"X-Auth-Token": st.secrets["X_AUTH_TOKEN"]}

def get_matches(competition_code="PL", season="2024"):
    url = f"https://api.football-data.org/v4/competitions/{competition_code}/matches?season={season}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("matches", [])
    else:
        return []

def get_last_matches_by_team(team_id, season="2023", limit=5):
    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED&limit={limit}&season={season}"
    response = requests.get(url, headers=HEADERS)

    print(f"Status: {response.status_code}")
    print(response.text)

    if response.status_code == 200:
        return response.json().get("matches", [])
    else:
        return []



#Função get pra busca por competição
def get_teams_by_competition(competition_code):
    url = f"https://api.football-data.org/v4/competitions/{competition_code}/teams"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("teams", [])
    return []
