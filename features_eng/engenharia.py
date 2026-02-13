import pandas as pd
import numpy as np
import sys
import os

# Adiciona diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from uteis.logger import logger_principal

def criar_features(df):
    """
    Cria novas features para o modelo.
    """
    logger_principal.info("Iniciando engenharia de features...")
    
    # Preço por m2 (útil para análise, talvez não para treino se for vazar target, mas ok para EDA)
    df['preco_m2'] = df['preco'] / df['area']
    
    # Log do preço (target) para normalizar distribuição
    df['log_preco'] = np.log1p(df['preco'])
    
    # Log da área
    df['log_area'] = np.log1p(df['area'])
    
    # Tratamento de Bairro
    # Vamos manter o nome original para visualização
    # Mas criar dummies para o modelo
    # Se houver muitos bairros, agrupar os pequenos em "Outros"
    contagem_bairros = df['bairro'].value_counts()
    bairros_comuns = contagem_bairros[contagem_bairros > 5].index # Pelo menos 5 ocorrências
    
    df['bairro_tratado'] = df['bairro'].apply(lambda x: x if x in bairros_comuns else 'Outros')
    
    # One-Hot Encoding
    df = pd.get_dummies(df, columns=['bairro_tratado'], prefix='bairro', drop_first=True)
    
    # Se tiver lat/lon, podemos criar features espaciais?
    # Por enquanto mantemos apenas lat/lon originais se existirem
    
    logger_principal.info(f"Engenharia de features concluída. Colunas: {list(df.columns)}")
    return df
