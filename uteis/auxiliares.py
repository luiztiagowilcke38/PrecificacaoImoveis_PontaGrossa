import pandas as pd
import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from configuracao import DIRETORIO_IMAGENS, DIRETORIO_DADOS

def salvar_grafico(fig, nome_arquivo):
    """Salva uma figura matplotlib no diretório de imagens."""
    caminho = os.path.join(DIRETORIO_IMAGENS, nome_arquivo)
    fig.savefig(caminho, bbox_inches='tight', dpi=300)
    print(f"Gráfico salvo em: {caminho}")

def salvar_modelo(modelo, nome_arquivo):
    """Salva um modelo treinado usando pickle."""
    caminho = os.path.join(DIRETORIO_DADOS, nome_arquivo)
    with open(caminho, 'wb') as f:
        pickle.dump(modelo, f)
    print(f"Modelo salvo em: {caminho}")

def carregar_modelo(nome_arquivo):
    """Carrega um modelo treinado."""
    caminho = os.path.join(DIRETORIO_DADOS, nome_arquivo)
    if os.path.exists(caminho):
        with open(caminho, 'rb') as f:
            return pickle.load(f)
    return None

def formatar_moeda(valor):
    """Formata valor para BRL."""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
