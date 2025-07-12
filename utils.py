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




#### Tendencias
def detectar_tendencias(df):
    tendencias = []

    # Últimos 5 jogos
    ultimos = df.head(5)

    # Tendência de vitórias consecutivas
    sequencia = "".join(ultimos["Resultado"].tolist())
    if sequencia.startswith("VitóriaVitóriaVitória"):
        tendencias.append("📈 Vem de 3 vitórias consecutivas")

    if sequencia.startswith("DerrotaDerrotaDerrota"):
        tendencias.append("📉 Vem de 3 derrotas consecutivas")

    # Tendência fora de casa
    ult_fora = ultimos[ultimos["Local"] == "Fora"]
    if len(ult_fora) >= 3 and all(ult_fora["Resultado"].iloc[:3] == "Derrota"):
        tendencias.append("🛑 Perdeu os últimos 3 jogos fora de casa")

    # Sem marcar gols
    if (ultimos["Gols Marcados"] == 0).sum() >= 2:
        tendencias.append("⚠️ Não marcou gols em 2 dos últimos 5 jogos")

    return tendencias
