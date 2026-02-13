import pandas as pd
import numpy as np
import os
from configuracao import DIRETORIO_DADOS
from dados.carregador import carregar_dados_com_pois

def limpar_dados(df=None):
    """
    Realiza a limpeza e tratamento de dados.
    - Remove duplicatas
    - Trata nulos (imputação pela mediana do bairro)
    - Remove outliers (IQR method)
    - Converte tipos de dados
    """
    if df is None:
        df = carregar_dados_com_pois()

    print(f"Dados originais: {df.shape}")

    # 1. Remover duplicatas
    df.drop_duplicates(inplace=True)

    # 2. Conversão de Tipos
    colunas_numericas = ['preco', 'area', 'quartos', 'banheiros', 'vagas']
    for col in colunas_numericas:
        if col in df.columns:
            # Força conversão para numérico, erros viram NaN
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # 3. Tratamento de Nulos
    # Remove linhas onde preço ou área são nulos (essenciais)
    df.dropna(subset=['preco', 'area'], inplace=True)
    
    # Preenche nulos em quartos/banheiros/vagas com a mediana do bairro se possível, senão da cidade
    for col in ['quartos', 'banheiros', 'vagas']:
        if col in df.columns:
            df[col] = df.groupby('bairro')[col].transform(lambda x: x.fillna(x.median()))
            df[col] = df[col].fillna(df[col].median()) # Fallback global

    # 4. Feature Engineering Básica (Preço por m2)
    df['preco_m2'] = df['preco'] / df['area']

    # 5. Remoção de Outliers (Preço e Área)
    # Remove imóveis com preço < 10.000 (erro de digitação provável)
    df = df[df['preco'] > 10000]
    
    # IQR para Preço/m2
    Q1 = df['preco_m2'].quantile(0.05)
    Q3 = df['preco_m2'].quantile(0.95)
    IQR = Q3 - Q1
    limite_inferior = Q1 - 1.5 * IQR
    limite_superior = Q3 + 1.5 * IQR
    
    df = df[(df['preco_m2'] >= limite_inferior) & (df['preco_m2'] <= limite_superior)]

    print(f"Dados pós-limpeza: {df.shape}")
    
    # Salvar
    caminho = os.path.join(DIRETORIO_DADOS, 'dados_limpos.csv')
    df.to_csv(caminho, index=False)
    
    return df

if __name__ == "__main__":
    limpar_dados()
