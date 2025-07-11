import streamlit as st
from datetime import date
from registro import salvar_aposta, carregar_apostas


###Formulario de registro de Apostas
st.title("📋 Registro de Apostas - BetInsight")

st.subheader("Adicionar nova aposta")

data_aposta = st.date_input("Data da aposta", value=date.today())
jogo = st.text_input("Jogo (ex: Flamengo x Fluminense)")
mercado = st.selectbox("Mercado", ["Over 2.5", "Ambas Marcam", "Resultado Final", "Escanteios", "Outro"])
valor = st.number_input("Valor apostado (R$)", min_value=1.0, step=1.0)
odd = st.number_input("Odd", min_value=1.01, step=0.01)
resultado = st.selectbox("Resultado", ["Ganhou", "Perdeu"])

if st.button("Salvar aposta"):
    aposta = {
        "data": data_aposta.strftime("%Y-%m-%d"),
        "jogo": jogo,
        "mercado": mercado,
        "valor": valor,
        "odd": odd,
        "resultado": resultado
    }
    salvar_aposta(aposta)
    st.success("✅ Aposta salva com sucesso!")

# Visualizar apostas já registradas
st.subheader("📄 Histórico de Apostas")
df_apostas = carregar_apostas()
st.dataframe(df_apostas)


import plotly.express as px
import pandas as pd
### filtros do dashboard
st.subheader("🧮 Filtros")

if not df_apostas.empty:
    df = df_apostas.copy()
    df["data"] = pd.to_datetime(df["data"])

    # Filtro de data
    min_data = df["data"].min().date()
    max_data = df["data"].max().date()

    data_inicio, data_fim = st.date_input("Período", value=(min_data, max_data))

    # Filtro de mercado
    mercados = df["mercado"].unique().tolist()
    mercado_selecionado = st.multiselect("Mercados", mercados, default=mercados)

    # Aplicar filtros
    df = df[
        (df["data"] >= pd.to_datetime(data_inicio)) &
        (df["data"] <= pd.to_datetime(data_fim)) &
        (df["mercado"].isin(mercado_selecionado))
    ]



###Dashboard e métricas

st.subheader("📊 Análise de Desempenho")

if not df_apostas.empty:
    # Conversões necessárias
    df = df_apostas.copy()
    df["ganhou"] = df["resultado"] == "Ganhou"
    df["ganho"] = df.apply(lambda row: (row["valor"] * (row["odd"] - 1)) if row["ganhou"] else -row["valor"], axis=1)
    df["data"] = pd.to_datetime(df["data"])

    lucro_total = df["ganho"].sum()
    total_apostado = df["valor"].sum()
    taxa_acerto = df["ganhou"].mean() * 100
    roi = (lucro_total / total_apostado) * 100 if total_apostado else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Lucro total", f"R$ {lucro_total:.2f}")
    col2.metric("🎯 Acerto", f"{taxa_acerto:.1f}%")
    col3.metric("📈 ROI", f"{roi:.1f}%")

    # Gráfico de evolução do lucro
    df["lucro_acumulado"] = df["ganho"].cumsum()
    fig_lucro = px.line(df.sort_values("data"), x="data", y="lucro_acumulado", title="Evolução do Lucro")
    st.plotly_chart(fig_lucro)

    # Gráfico pizza acerto x erro
    resultado_count = df["resultado"].value_counts()
    fig_pizza = px.pie(values=resultado_count.values, names=resultado_count.index, title="Acertos vs Erros")
    st.plotly_chart(fig_pizza)

    # Gráfico ROI por mercado
    df_roi_mercado = df.groupby("mercado").agg({
        "ganho": "sum",
        "valor": "sum"
    }).reset_index()
    df_roi_mercado["ROI (%)"] = (df_roi_mercado["ganho"] / df_roi_mercado["valor"]) * 100
    fig_roi = px.bar(df_roi_mercado, x="mercado", y="ROI (%)", title="ROI por Mercado", color="ROI (%)")
    st.plotly_chart(fig_roi)

else:
    st.info("Ainda não há apostas suficientes para análise.")
