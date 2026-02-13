import pandas as pd
import os
import sys

# Adiciona diretório raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from uteis.logger import logger_principal

def analise_temporal(df):
    """
    Realiza análise temporal se houver data.
    """
    if 'data_coleta' not in df.columns:
        logger_principal.warning("Coluna 'data_coleta' não encontrada. Pulando análise temporal.")
        return None
    
    # Placeholder para logica futura
    df['data_coleta'] = pd.to_datetime(df['data_coleta'])
    df_temporal = df.groupby(df['data_coleta'].dt.to_period('M'))['preco'].mean()
    
    return df_temporal
