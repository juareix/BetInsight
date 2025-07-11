import streamlit as st
from datetime import date
from registro import salvar_aposta, carregar_apostas

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