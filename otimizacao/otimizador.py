from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
import sys
import os

# Adiciona diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from uteis.logger import logger_principal

def otimizar_random_forest(X_train, y_train):
    """
    Otimiza hiperparâmetros do Random Forest.
    """
    logger_principal.info("Iniciando otimização de hiperparâmetros (Random Forest)...")
    
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    
    rf = RandomForestRegressor(random_state=42)
    
    search = RandomizedSearchCV(estimator=rf, param_distributions=param_grid, 
                                n_iter=10, cv=3, verbose=2, random_state=42, n_jobs=-1)
                                
    search.fit(X_train, y_train)
    
    logger_principal.info(f"Melhores parâmetros encontrados: {search.best_params_}")
    logger_principal.info(f"Melhor score (CV): {search.best_score_:.4f}")
    
    return search.best_estimator_
