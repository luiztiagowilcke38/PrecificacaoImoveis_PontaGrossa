import folium
import pandas as pd
import os
import sys

# Adiciona diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configuracao import DIRETORIO_IMAGENS

def gerar_mapa(df):
    """
    Gera um mapa HTML com os imóveis.
    """
    print("Gerando mapa interativo...")
    
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        print("Colunas de latitude/longitude não encontradas. Mapa não será gerado.")
        return
        
    # Centro do mapa (média das coordenadas)
    lat_media = df['latitude'].mean()
    lon_media = df['longitude'].mean()
    
    m = folium.Map(location=[lat_media, lon_media], zoom_start=13)
    
    # Amostra para não poluir muito se for grande
    df_sample = df.sample(min(1000, len(df)))
    
    for idx, row in df_sample.iterrows():
        try:
            preco_fmt = f"R$ {row['preco']:,.2f}"
            popup_html = f"""
            <b>{row['bairro']}</b><br>
            Preço: {preco_fmt}<br>
            Área: {row['area']}m²<br>
            Quartos: {row['quartos']}
            """
            
            # Cor baseada no preço (simples)
            cor = 'blue'
            if row['preco'] > df['preco'].quantile(0.75):
                cor = 'red'
            elif row['preco'] < df['preco'].quantile(0.25):
                cor = 'green'
                
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=5,
                popup=folium.Popup(popup_html, max_width=300),
                color=cor,
                fill=True,
                fill_color=cor
            ).add_to(m)
            
        except Exception as e:
            continue
            
    caminho_mapa = os.path.join(DIRETORIO_IMAGENS, 'mapa_imoveis.html')
    m.save(caminho_mapa)
    print(f"Mapa salvo em {caminho_mapa}")
