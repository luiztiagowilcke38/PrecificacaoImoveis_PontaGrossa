import pandas as pd
import os
import sys

# Adiciona diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from configuracao import DIRETORIO_DADOS
from uteis.logger import logger_principal
from dados.geocodificador import geocodificar_imoveis
from dados.poi import calcular_distancias_pois
from features_eng.limpeza import limpar_dados
from features_eng.engenharia import criar_features
from analise.eda import realizar_eda
from modelos.treinamento import treinar_modelos
from visualizacao.graficos import plotar_resultados, plotar_importancia_features
from visualizacao.mapas import gerar_mapa
from modelos.timeseries.forecasting import analise_temporal

def main():
    logger_principal.info("Iniciando Pipeline do Modelo de Avaliação de Imóveis")
    
    # 1. Verificar Dados Brutos
    arquivo_bruto = os.path.join(DIRETORIO_DADOS, 'dados_brutos.csv')
    if not os.path.exists(arquivo_bruto):
        logger_principal.error("Dados brutos não encontrados. Execute o raspador primeiro.")
        return

    # 2. Geocodificação (se necessário)
    arquivo_geo = os.path.join(DIRETORIO_DADOS, 'dados_geocodificados.csv')
    if not os.path.exists(arquivo_geo):
        logger_principal.info("Executando geocodificação...")
        geocodificar_imoveis()
    
    # 3. POIs (se necessário)
    arquivo_poi = os.path.join(DIRETORIO_DADOS, 'dados_com_pois.csv')
    if not os.path.exists(arquivo_poi):
         logger_principal.info("Calculando POIs...")
         calcular_distancias_pois()
    
    # Carregar dados (prioridade: POI > Geo > Bruto)
    if os.path.exists(arquivo_poi):
        df = pd.read_csv(arquivo_poi)
        logger_principal.info("Dados carregados com features de POI.")
    elif os.path.exists(arquivo_geo):
        df = pd.read_csv(arquivo_geo)
        logger_principal.info("Dados carregados com geocodificação.")
    else:
        df = pd.read_csv(arquivo_bruto)
        logger_principal.info("Dados brutos carregados.")
        
    # 4. Limpeza
    df = limpar_dados(df)
    
    # 5. Engenharia de Features
    df = criar_features(df)
    
    # Salvar dados processados para inspeção
    df.to_csv(os.path.join(DIRETORIO_DADOS, 'dados_processados.csv'), index=False)
    
    # 6. EDA
    realizar_eda(df)
    
    # 6.1 Análise Temporal (Se houver dados)
    analise_temporal(df)
    
    # 7. Visualização (Mapa)
    gerar_mapa(df)
    
    # 8. Treinamento e Avaliação
    resultados, features, best_model, X_test, y_test = treinar_modelos(df)
    
    # 9. Visualização de Resultados
    for nome, res in resultados.items():
        plotar_resultados(res['y_test'], res['y_pred'], nome)
        
    # Importância das features (apenas para o melhor modelo se for tree-based)
    if hasattr(best_model, 'feature_importances_'):
        plotar_importancia_features(best_model, features, 'Melhor Modelo')

    logger_principal.info("Pipeline finalizado com sucesso!")

if __name__ == "__main__":
    main()
