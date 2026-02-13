from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import sys
import os

# Adiciona diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from uteis.logger import logger_principal

def avaliar_modelo_detalhado(modelo, X_test, y_test, nome_modelo="Modelo"):
    """
    Gera um relatório detalhado de avaliação.
    """
    y_pred = modelo.predict(X_test)
    
    # Métricas Log
    mse_log = mean_squared_error(y_test, y_pred)
    rmse_log = np.sqrt(mse_log)
    r2 = r2_score(y_test, y_pred)
    
    # Métricas Reais
    y_test_orig = np.expm1(y_test)
    y_pred_orig = np.expm1(y_pred)
    
    mae_real = mean_absolute_error(y_test_orig, y_pred_orig)
    rmse_real = np.sqrt(mean_squared_error(y_test_orig, y_pred_orig))
    mape = np.mean(np.abs((y_test_orig - y_pred_orig) / y_test_orig)) * 100
    
    relatorio = f"""
    === Relatório de Avaliação: {nome_modelo} ===
    R2 Score: {r2:.4f} (Quanto maior, melhor)
    RMSE (Log): {rmse_log:.4f}
    
    Métricas na Escala Real (R$):
    - MAE (Erro Médio Absoluto): R$ {mae_real:.2f}
    - RMSE (Erro Quadrático Médio): R$ {rmse_real:.2f}
    - MAPE (Erro Percentual Médio): {mape:.2f}%
    
    Interpretação:
    O modelo erra, em média, {mape:.2f}% do valor do imóvel.
    Para um imóvel de R$ 300.000, o erro médio é de +/- R$ {mae_real:.2f}.
    =============================================
    """
    
    logger_principal.info(relatorio)
    print(relatorio)
    
    return {
        'r2': r2,
        'rmse_log': rmse_log,
        'mae_real': mae_real,
        'rmse_real': rmse_real,
        'mape': mape
    }
