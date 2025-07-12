import pandas as pd

def partidas_para_df(partidas, team_id):
    dados = []

    for p in partidas:
        casa = p["homeTeam"]["id"] == team_id
        placar_casa = p["score"]["fullTime"]["home"]
        placar_fora = p["score"]["fullTime"]["away"]
        
        dados.append({
            "Data": p["utcDate"][:10],
            "Adversário": p["awayTeam"]["name"] if casa else p["homeTeam"]["name"],
            "Local": "Casa" if casa else "Fora",
            "Placar": f"{placar_casa} x {placar_fora}",
            "Resultado": resultado_jogo(placar_casa, placar_fora, casa),
            "Gols Marcados": placar_casa if casa else placar_fora,
            "Gols Sofridos": placar_fora if casa else placar_casa
        })

    return pd.DataFrame(dados)

def resultado_jogo(gols_casa, gols_fora, foi_casa):
    if gols_casa == gols_fora:
        return "Empate"
    elif (gols_casa > gols_fora and foi_casa) or (gols_fora > gols_casa and not foi_casa):
        return "Vitória"
    else:
        return "Derrota"

def calcular_medias_gols(df):
    return df["Gols Marcados"].mean(), df["Gols Sofridos"].mean()
