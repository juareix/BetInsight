import pandas as pd
from datetime import datetime
import os

ARQUIVO_APOSTAS = "data/apostas.csv"

def salvar_aposta(aposta):
    df = pd.DataFrame([aposta])
    
    if os.path.exists(ARQUIVO_APOSTAS):
        df_existente = pd.read_csv(ARQUIVO_APOSTAS)
        df_total = pd.concat([df_existente, df], ignore_index=True)
    else:
        df_total = df
    
    df_total.to_csv(ARQUIVO_APOSTAS, index=False)

def carregar_apostas():
    if os.path.exists(ARQUIVO_APOSTAS):
        return pd.read_csv(ARQUIVO_APOSTAS)
    else:
        return pd.DataFrame()
