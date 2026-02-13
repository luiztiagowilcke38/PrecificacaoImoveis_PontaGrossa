from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import os
import sys

# Adiciona diretório raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from configuracao import SEED

def get_random_forest():
    """Retorna o modelo Random Forest configurado."""
    return RandomForestRegressor(n_estimators=100, random_state=SEED)

def get_gradient_boosting():
    """Retorna o modelo Gradient Boosting configurado."""
    return GradientBoostingRegressor(n_estimators=100, random_state=SEED)
