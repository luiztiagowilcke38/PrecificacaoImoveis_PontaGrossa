from sklearn.linear_model import LinearRegression, Ridge, Lasso
import sys
import os

# Adiciona diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# Correção: 2 dirname para sair de modelos/linear -> modelos -> raiz
# Na verdade, __file__ está em modelos/linear/regressores.py
# modelos/linear -> modelos -> ModeloPonta (raiz)
# Então são 3 dirnames. Vamos testar.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def treinar_linear(X_train, y_train):
    """
    Treina uma Regressão Linear simples.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def treinar_ridge(X_train, y_train, alpha=1.0):
    """
    Treina Regressão Ridge (L2).
    """
    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)
    return model

def treinar_lasso(X_train, y_train, alpha=0.1):
    """
    Treina Regressão Lasso (L1).
    """
    model = Lasso(alpha=alpha)
    model.fit(X_train, y_train)
    return model
