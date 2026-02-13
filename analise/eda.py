import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os

# Adiciona diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configuracao import DIRETORIO_IMAGENS

def realizar_eda(df):
    """
    Realiza Análise Exploratória de Dados e salva gráficos.
    """
    print("Iniciando EDA...")
    
    # Configurar estilo
    sns.set(style="whitegrid")
    
    # 1. Distribuição de Preços
    plt.figure(figsize=(10, 6))
    sns.histplot(df['preco'], kde=True, bins=30)
    plt.title('Distribuição de Preços dos Imóveis')
    plt.xlabel('Preço (R$)')
    plt.savefig(os.path.join(DIRETORIO_IMAGENS, 'distribuicao_precos.png'))
    plt.close()
    
    # 2. Distribuição de Área
    plt.figure(figsize=(10, 6))
    # Filtrar áreas muito grandes para visualização
    sns.histplot(df[df['area'] < 500]['area'], kde=True, bins=30)
    plt.title('Distribuição de Áreas (até 500m²)')
    plt.xlabel('Área (m²)')
    plt.savefig(os.path.join(DIRETORIO_IMAGENS, 'distribuicao_areas.png'))
    plt.close()
    
    # 3. Preço vs Área (Scatter)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='area', y='preco', data=df)
    plt.title('Preço vs Área')
    plt.xlabel('Área (m²)')
    plt.ylabel('Preço (R$)')
    plt.savefig(os.path.join(DIRETORIO_IMAGENS, 'preco_vs_area.png'))
    plt.close()
    
    # 4. Matriz de Correlação
    plt.figure(figsize=(12, 10))
    # Selecionar apenas colunas numéricas
    cols_num = df.select_dtypes(include=['float64', 'int64']).columns
    corr = df[cols_num].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de Correlação')
    plt.savefig(os.path.join(DIRETORIO_IMAGENS, 'correlacao.png'))
    plt.close()
    
    print("EDA concluída. Gráficos salvos em imagens/")
