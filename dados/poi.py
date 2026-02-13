import pandas as pd
import osmnx as ox # type: ignore
import networkx as nx
from geopy.distance import geodesic # type: ignore
import pandas as pd
import numpy as np
import os
import sys

# Adiciona o diretório raiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configuracao import DIRETORIO_DADOS, NOME_CIDADE, NOME_ESTADO, NOME_PAIS

def buscar_pois():
    """Busca POIs reais de Ponta Grossa no OpenStreetMap."""
    lugar = f"{NOME_CIDADE}, {NOME_ESTADO}, {NOME_PAIS}"
    print(f"Buscando POIs em {lugar} via OSMnx...")

    tags = {
        'amenity': ['school', 'hospital', 'pharmacy', 'marketplace', 'restaurant'],
        'leisure': ['park']
    }
    
    try:
        pois = ox.features_from_place(lugar, tags=tags)
        
        # Filtra apenas pontos (nós) ou centroides de polígonos
        pois['centroide'] = pois.geometry.centroid
        pois['lat'] = pois.centroide.y
        pois['lon'] = pois.centroide.x
        
        # Mantém apenas colunas relevantes
        if 'amenity' in pois.columns and 'leisure' in pois.columns:
            pois['tipo'] = pois['amenity'].fillna(pois['leisure'])
        elif 'amenity' in pois.columns:
            pois['tipo'] = pois['amenity']
        elif 'leisure' in pois.columns:
            pois['tipo'] = pois['leisure']
        else:
            pois['tipo'] = 'desconhecido'

        df_pois = pois[['tipo', 'lat', 'lon']].copy()
        df_pois.reset_index(drop=True, inplace=True)
        
        return df_pois

    except Exception as e:
        print(f"Erro ao baixar POIs: {e}")
        return pd.DataFrame()

def calcular_distancias_pois(arquivo_imoveis='dados_geocodificados.csv', arquivo_saida='dados_com_pois.csv'):
    """Calcula distâncias dos imóveis para os POIs mais próximos."""
    caminho_entrada = os.path.join(DIRETORIO_DADOS, arquivo_imoveis)
    if not os.path.exists(caminho_entrada):
        print(f"Arquivo {caminho_entrada} não encontrado.")
        return

    df_imoveis = pd.read_csv(caminho_entrada)
    df_pois = buscar_pois()

    if df_pois.empty:
        print("Nenhum POI encontrado. Pulando etapa.")
        return

    print("Calculando distâncias para POIs...")

    # Separa POIs por categoria
    escolas = df_pois[df_pois['tipo'] == 'school']
    hospitais = df_pois[df_pois['tipo'] == 'hospital']
    parques = df_pois[df_pois['tipo'] == 'park']
    farmacias = df_pois[df_pois['tipo'] == 'pharmacy']

    def dist_minima(row, df_alvos):
        if df_alvos.empty:
            return 9999.0
        
        # Vetorização seria melhor, mas iterativo é mais simples para entender
        coords_imovel = (row['latitude'], row['longitude'])
        distancias = df_alvos.apply(lambda r: geodesic(coords_imovel, (r['lat'], r['lon'])).meters, axis=1)
        return distancias.min()

    def contar_raio(row, df_alvos, raio_m=500):
        if df_alvos.empty:
            return 0
        coords_imovel = (row['latitude'], row['longitude'])
        # Contagem aproximada (geodesic é lento para loop, usando aproximação Euclidiana rápida para pré-filtro se necessário, mas aqui vamos direto)
        # Para otimizar: calcular distâncias apenas se necessário. 
        # Aqui, vamos simplificar e usar a mesma lógica
        distancias = df_alvos.apply(lambda r: geodesic(coords_imovel, (r['lat'], r['lon'])).meters, axis=1)
        return (distancias <= raio_m).sum()

    # Aplica cálculos (pode demorar um pouco para 3500 imóveis)
    # Otimização: processar por lotes ou usar KDTree/BallTree do Scikit-Learn
    # Vamos usar BallTree por ser MUITO mais rápido que geodesic no loop
    from sklearn.neighbors import BallTree

    def calcular_features_rapido(df_imoveis, df_targets, prefixo):
        if df_targets.empty:
            df_imoveis[f'dist_{prefixo}'] = 9999
            df_imoveis[f'qtd_{prefixo}_500m'] = 0
            return

        # Converter para radianos
        imoveis_rad = np.deg2rad(df_imoveis[['latitude', 'longitude']].values)
        targets_rad = np.deg2rad(df_targets[['lat', 'lon']].values)

        tree = BallTree(targets_rad, metric='haversine')
        
        # Distância para o mais próximo (k=1)
        dist_rad, _ = tree.query(imoveis_rad, k=1)
        df_imoveis[f'dist_{prefixo}'] = dist_rad * 6371000 # Raio terra em metros

        # Quantidade em raio 500m
        count = tree.query_radius(imoveis_rad, r=500/6371000, count_only=True)
        df_imoveis[f'qtd_{prefixo}_500m'] = count

    calcular_features_rapido(df_imoveis, escolas, 'escola')
    calcular_features_rapido(df_imoveis, hospitais, 'hospital')
    calcular_features_rapido(df_imoveis, parques, 'parque')
    calcular_features_rapido(df_imoveis, farmacias, 'farmacia')

    # Criação de Scores
    # score_educacao = 1 / (1 + dist) + 0.5 * qtd
    df_imoveis['score_educacao'] = (1000 / (100 + df_imoveis['dist_escola'])) + (0.5 * df_imoveis['qtd_escola_500m'])
    df_imoveis['score_lazer'] = (1000 / (100 + df_imoveis['dist_parque'])) + (0.5 * df_imoveis['qtd_parque_500m'])
    df_imoveis['score_saude'] = (1000 / (100 + df_imoveis['dist_hospital'])) + (0.5 * df_imoveis['qtd_hospital_500m'])

    caminho_saida = os.path.join(DIRETORIO_DADOS, arquivo_saida)
    df_imoveis.to_csv(caminho_saida, index=False)
    print(f"Enriquecimento com POIs concluído! Salvo em {caminho_saida}")

if __name__ == "__main__":
    calcular_distancias_pois()
