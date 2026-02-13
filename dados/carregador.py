import pandas as pd
import os
import sys
from configuracao import DIRETORIO_DADOS

def carregar_dados_brutos():
    """Carrega o dataset bruto (scrapeado ou sintético)."""
    caminho = os.path.join(DIRETORIO_DADOS, 'dados_brutos.csv')
    if os.path.exists(caminho):
        return pd.read_csv(caminho)
    else:
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

def carregar_dados_com_pois():
    """Carrega o dataset enriquecido com POIs."""
    caminho = os.path.join(DIRETORIO_DADOS, 'dados_com_pois.csv')
    if os.path.exists(caminho):
        return pd.read_csv(caminho)
    else:
        # Tenta carregar o bruto se o enriquecido não existir (fallback)
        print("Aviso: dados_com_pois.csv não encontrado. Tentando carregar dados_brutos.csv")
        return carregar_dados_brutos()

def carregar_dados_processados():
    """Carrega o dataset final processado para modelagem."""
    caminho = os.path.join(DIRETORIO_DADOS, 'dados_processados.csv')
    if os.path.exists(caminho):
        return pd.read_csv(caminho)
    return None
