import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
import sys

# Adiciona diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configuracao import DIRETORIO_IMAGENS

def plotar_resultados(y_test, y_pred, nome_modelo):
    """
    Plota Gráfico de Predito vs Real.
    """
    plt.figure(figsize=(10, 6))
    
    # Voltar para escala original se estiver em log
    y_test_orig = np.expm1(y_test)
    y_pred_orig = np.expm1(y_pred)
    
    plt.scatter(y_test_orig, y_pred_orig, alpha=0.5)
    
    # Linha ideal
    max_val = max(y_test_orig.max(), y_pred_orig.max())
    min_val = min(y_test_orig.min(), y_pred_orig.min())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--')
    
    plt.xlabel('Preço Real (R$)')
    plt.ylabel('Preço Predito (R$)')
    plt.title(f'Real vs Predito - {nome_modelo}')
    
    plt.savefig(os.path.join(DIRETORIO_IMAGENS, f'predicao_{nome_modelo}.png'))
    plt.close()

def plotar_importancia_features(modelo, features_names, nome_modelo):
    """
    Plota importância das features.
    """
    if not hasattr(modelo, 'feature_importances_'):
        return

    importances = modelo.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x=importances[indices], y=[features_names[i] for i in indices])
    plt.title(f'Importância das Features - {nome_modelo}')
    plt.xlabel('Importância')
    plt.tight_layout()
    plt.savefig(os.path.join(DIRETORIO_IMAGENS, f'importancia_features_{nome_modelo}.png'))
    plt.close()
