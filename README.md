# Modelo de Avaliação de Imóveis - Ponta Grossa/PR
---
**Autor**: Luiz Tiago Wilcke

Este projeto implementa um pipeline completo de Data Science para a avaliação (precificação) de imóveis na cidade de Ponta Grossa, Paraná. Utiliza dados reais coletados de portais imobiliários e os enriquece com informações de pontos de interesse (escolas, hospitais, parques) via OpenStreetMap.

## 📋 Funcionalidades

O sistema é modular e abrange todas as etapas de um projeto de Machine Learning:

1.  **Coleta de Dados (Web Scraping)**: Script para extrair anúncios da OLX.
2.  **Geocodificação**: Atribuição de coordenadas geográficas baseadas no bairro.
3.  **Enriquecimento (Feature Engineering)**:
    *   Cálculo de distância para amenidades urbanas (escolas, hospitais, farmácias).
    *   Criação de Scores de Localização (Educação, Saúde, Lazer).
4.  **Limpeza e Tratamento**: Remoção de outliers, tratamento de nulos e conversão de tipos.
5.  **Modelagem Preditiva**:
    *   **Ensemble**: Random Forest, Gradient Boosting.
    *   **Lineares**: Ridge, Lasso.
    *   **Não-Lineares**: MLP (Redes Neurais).
6.  **Otimização**: Ajuste fino de hiperparâmetros (GridSearch).
7.  **Visualização**:
    *   Mapas interativos de calor e localização.
    *   Gráficos de distribuição e correlação.

## 🚀 Como Executar

Certifique-se de ter o Python 3.12+ instalado.

1.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    # Ou manualmente:
    pip install pandas numpy scikit-learn matplotlib seaborn folium osmnx geopy plotly playwright
    ```

2.  **Execute o Pipeline Principal**:
    Este comando executará todas as etapas (limpeza -> engenharia -> treino -> avaliação).
    ```bash
    python main.py
    ```

## 📊 Resultados Obtidos

O modelo foi avaliado utilizando métricas robustas (RMSE, MAE, R2). O melhor desempenho foi obtido com o algoritmo **Gradient Boosting**.

| Modelo | R2 Score | MAE (Erro Médio) | RMSE (Erro Quadrático) |
| :--- | :--- | :--- | :--- |
| **Gradient Boosting** | **0.66** | **R$ 57.021** | **R$ 110.000** |
| Random Forest | 0.62 | R$ 59.826 | R$ 115.000 |
| Regressão Linear | 0.57 | R$ 67.900 | R$ 123.000 |

*Obs: O MAE indica que o modelo erra, em média, cerca de R$ 57 mil para mais ou para menos no valor do imóvel.*

## � Modelagem Matemática

O projeto utiliza algoritmos avançados de regressão. Abaixo estão as formulações matemáticas dos principais modelos e métricas utilizadas.

### 1. Gradient Boosting (Melhor Modelo)
O Gradient Boosting constrói um modelo aditivo de forma sequencial, onde cada nova árvore tenta corrigir os erros (resíduos) da anterior.

$$ F_m(x) = F_{m-1}(x) + \gamma_m h_m(x) $$

Onde:
*   $F_m(x)$ é a predição na iteração $m$.
*   $h_m(x)$ é a nova árvore de decisão (weak learner).
*   $\gamma_m$ é a taxa de aprendizado (learning rate) que controla a contribuição de cada árvore.

A função de perda otimizada é o Erro Quadrático Médio (MSE):
$$ L(y, F(x)) = \frac{1}{2}(y - F(x))^2 $$

### 2. Random Forest
O Random Forest é um método de *bagging* que cria múltiplas árvores de decisão independentes e calcula a média de suas predições para reduzir a variância.

$$ \hat{y} = \frac{1}{B} \sum_{b=1}^{B} f_b(x) $$

Onde:
*   $B$ é o número total de árvores.
*   $f_b(x)$ é a predição da $b$-ésima árvore treinada em uma amostra *bootstrap* dos dados.

### 3. Métricas de Avaliação
Para validar a performance, utilizamos as seguintes métricas:

**Root Mean Squared Error (RMSE)**:
$$ RMSE = \sqrt{\frac{1}{n} \sum_{i=1}^{n} (y_i - \hat{y}_i)^2} $$

**Coeficiente de Determinação ($R^2$)**:
$$ R^2 = 1 - \frac{\sum_{i=1}^{n} (y_i - \hat{y}_i)^2}{\sum_{i=1}^{n} (y_i - \bar{y})^2} $$

## �📂 Estrutura do Projeto

```
ModeloPonta/
├── analise/          # Análise Exploratória (EDA)
├── avaliacao/        # Métricas e relatórios detalhados
├── dados/            # Scripts de coleta e POIs
├── dados_arquivos/   # Datasets (brutos e processados)
├── features_eng/     # Engenharia de atributos
├── imagens/          # Gráficos e mapas gerados
├── modelos/          # Algoritmos de ML (salvos e scripts)
├── otimizacao/       # Ajuste de hiperparâmetros
├── uteis/            # Configurações e logs
├── visualizacao/     # Scripts de plotagem
└── main.py           # Orquestrador principal
```

## 🗺️ Visualizações

Os gráficos e mapas gerados são salvos automaticamente na pasta `imagens/`.
-   **mapa_imoveis.html**: Mapa interativo com a localização e preço dos imóveis.
-   **predicao_GradientBoosting.png**: Comparativo entre Valor Real vs Valor Predito.



