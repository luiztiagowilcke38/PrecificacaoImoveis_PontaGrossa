from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
import os
import sys

# Adiciona diretório raiz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from configuracao import SEED

def get_svr():
    """Retorna SVM Regressor."""
    # SVR precisa de scale, idealmente usar Pipeline.
    # Aqui retornamos raw.
    return SVR(C=1.0, epsilon=0.2)

def get_mlp():
    """Retorna MLP Regressor."""
    return MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=SEED)
