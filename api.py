# api.py
import requests

API_TOKEN = "51942df7d44e4191a84466cecfbc7bec"
HEADERS = {"X-Auth-Token": API_TOKEN}

def get_matches(competition_code="PL", season="2024"):
    url = f"https://api.football-data.org/v4/competitions/{competition_code}/matches?season={season}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("matches", [])
    else:
        return []



#Função para pegar os ultimso resultados dos times:
def get_last_matches_by_team(team_id, limit=5):
    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?status=FINISHED&limit={limit}"
    response = requests.get(url, headers=HEADERS)
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
