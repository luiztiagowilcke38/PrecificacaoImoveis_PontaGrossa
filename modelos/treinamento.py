import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import sys
import os

# Adiciona diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configuracao import DIRETORIO_MODELOS, SEED, TAMANHO_TESTE
from uteis.logger import logger_principal

# Imports dos Módulos criadaos
from modelos.ensemble.regressores import get_random_forest, get_gradient_boosting
from modelos.linear.regressores import treinar_ridge, treinar_lasso
from modelos.nonlinear.regressores import get_mlp
from otimizacao.otimizador import otimizar_random_forest
from avaliacao.avaliador import avaliar_modelo_detalhado

def treinar_modelos(df, otimizar=False):
    """
    Treina modelos de regressão e avalia.
    """
    logger_principal.info("Iniciando treinamento de modelos...")
    
    target = 'log_preco'
    # Remover colunas que não são features
    colunas_drop = ['preco', 'log_preco', 'preco_m2', 'endereco', 'titulo', 'bairro', 'bairro_tratado', 
                    'log_area', 'latitude', 'longitude']
    
    features = [c for c in df.columns if c not in colunas_drop]
    
    X = df[features]
    y = df[target]
    
    # Preencher NaNs remanescentes (segurança)
    X = X.fillna(0)
    
    logger_principal.info(f"Features selecionadas ({len(features)}): {features}")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TAMANHO_TESTE, random_state=SEED)
    
    # Dicionário de modelos para rodar
    modelos = {
        'RandomForest': get_random_forest(),
        'GradientBoosting': get_gradient_boosting(),
        'Ridge': treinar_ridge(X_train, y_train), # Já corre fit dentro, mas vamos padronizar
        'Lasso': treinar_lasso(X_train, y_train),
        'MLP': get_mlp()
    }
    
    # Se pedido otimização, substitui RF pelo otimizado
    if otimizar:
        logger_principal.info("Otimizando Random Forest...")
        rf_opt = otimizar_random_forest(X_train, y_train)
        modelos['RandomForest_Opt'] = rf_opt
    
    resultados = {}
    best_model = None
    best_score = -np.inf
    best_name = ""
    
    for nome, model in modelos.items():
        logger_principal.info(f"Avaliando {nome}...")
        
        # Alguns chamam fit, outros já retornaram treinado (linear), vamos garantir
        # Linear (neste code novo) retorna treinado. 
        # Ensemble retorna instancia nova.
        # Vamos padronizar: sempre chamar fit se tiver o método
        try:
             model.fit(X_train, y_train)
        except:
             pass # Já treinado
        
        # Avaliação Detalhada
        metricas = avaliar_modelo_detalhado(model, X_test, y_test, nome)
        
        y_pred = model.predict(X_test)
        
        resultados[nome] = {
            **metricas,
            'y_test': y_test,
            'y_pred': y_pred
        }
        
        if metricas['r2'] > best_score:
            best_score = metricas['r2']
            best_model = model
            best_name = nome
            
    logger_principal.info(f"Melhor modelo geral: {best_name} com R2: {best_score:.4f}")
    
    # Salvar melhor modelo
    caminho_modelo = os.path.join(DIRETORIO_MODELOS, 'melhor_modelo.pkl')
    joblib.dump(best_model, caminho_modelo)
    logger_principal.info(f"Modelo salvo em {caminho_modelo}")
    
    return resultados, features, best_model, X_test, y_test
