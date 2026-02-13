import pandas as pd
import numpy as np
import os
import sys

# Adiciona o diretório raiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configuracao import DIRETORIO_DADOS

def geocodificar_imoveis(arquivo_entrada='dados_brutos.csv', arquivo_saida='dados_geocodificados.csv'):
    """
    Adiciona coordenadas (lat/lon) aos imóveis baseado no bairro.
    Usa centroides aproximados dos bairros de Ponta Grossa para evitar
    geocodificação lenta de milhares de endereços fictícios.
    """
    caminho_entrada = os.path.join(DIRETORIO_DADOS, arquivo_entrada)
    if not os.path.exists(caminho_entrada):
        print(f"Arquivo {caminho_entrada} não encontrado.")
        return

    df = pd.read_csv(caminho_entrada)
    print(f"Carregando {len(df)} imóveis para geocodificação...")

    # Coordenadas aproximadas dos bairros de Ponta Grossa (Lat, Lon)
    # Obtidas via Google Maps/OSM manualmente para precisão
    coords_bairros = {
        "Centro": (-25.0916, -50.1668),
        "Oficinas": (-25.1150, -50.1450),
        "Uvaranas": (-25.0850, -50.1300),
        "Nova Russia": (-25.0800, -50.1800),
        "Jardim Carvalho": (-25.0750, -50.1550),
        "Estrela": (-25.1050, -50.1550),
        "Orfãs": (-25.0700, -50.1700),
        "Ronda": (-25.1000, -50.1850),
        "Boa Vista": (-25.0600, -50.1600),
        "Contorno": (-25.1200, -50.2000),
        "Neves": (-25.0500, -50.1400),
        "Chapada": (-25.0400, -50.1700),
        "Jardim America": (-25.1100, -50.1350),
        "Vila Estrela": (-25.1100, -50.1500),
        "Santo Antonio": (-25.0600, -50.1200),
        "Santa Paula": (-25.1300, -50.1800),
        "Jardim Sabara": (-25.0450, -50.1750),
        "Olarias": (-25.1000, -50.1400)
    }

    lats = []
    lons = []

    for bairro in df['bairro']:
        if bairro in coords_bairros:
            lat_base, lon_base = coords_bairros[bairro]
            # Adiciona ruído aleatório para distribuir os pontos no bairro (~500m)
            ruido_lat = np.random.normal(0, 0.003) 
            ruido_lon = np.random.normal(0, 0.003)
            lats.append(lat_base + ruido_lat)
            lons.append(lon_base + ruido_lon)
        else:
            # Centro da cidade como fallback
            lats.append(-25.0916)
            lons.append(-50.1668)

    df['latitude'] = lats
    df['longitude'] = lons

    caminho_saida = os.path.join(DIRETORIO_DADOS, arquivo_saida)
    df.to_csv(caminho_saida, index=False)
    print(f"Geocodificação concluída! Salvo em {caminho_saida}")

if __name__ == "__main__":
    geocodificar_imoveis()
