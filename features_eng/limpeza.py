import pandas as pd
import numpy as np
import sys
import os

# Adiciona diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from uteis.logger import logger_principal

def limpar_dados(df):
    """
    Realiza a limpeza básica dos dados.
    """
    logger_principal.info(f"Iniciando limpeza. Shape original: {df.shape}")
    
    # Remover duplicatas
    df = df.drop_duplicates()
    
    # Converter colunas numéricas
    cols_numericas = ['preco', 'area', 'quartos', 'banheiros', 'vagas']
    
    for col in cols_numericas:
        if df[col].dtype == object:
            # Remove caracteres não numéricos exceto ponto e virgula?
            # Assumindo formato '1000' ou '1.000' vindo do scraper
            # O scraper ja tentou limpar 'R$' e '.', mas vamos garantir
             df[col] = df[col].astype(str).str.replace(r'[^\d]', '', regex=True)
             df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Tratar valores nulos/zeros
    # Preço e Área não podem ser 0 ou Nulos
    df = df[df['preco'] > 0]
    df = df[df['area'] > 0]
    
    # Preencher nulos em quartos/banheiros/vagas com mediana ou 0
    df['quartos'] = df['quartos'].fillna(df['quartos'].median())
    df['banheiros'] = df['banheiros'].fillna(df['banheiros'].median())
    df['vagas'] = df['vagas'].fillna(0) # Assumir 0 se não informado
    
    # Remover outliers óbvios
    # Ex: Imoveis com area < 10m2 ou > 10000m2
    df = df[(df['area'] >= 10) & (df['area'] <= 10000)]
    
    # Ex: Preco < 10.000 (muito barato, erro?)
    df = df[df['preco'] >= 10000]
    
    logger_principal.info(f"Limpeza concluída. Shape final: {df.shape}")
    return df
