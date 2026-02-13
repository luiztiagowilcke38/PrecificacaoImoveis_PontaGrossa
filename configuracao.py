import os

# Configurações Gerais
DIRETORIO_BASE = os.path.dirname(os.path.abspath(__file__))
DIRETORIO_DADOS = os.path.join(DIRETORIO_BASE, 'dados_arquivos')
DIRETORIO_LOGS = os.path.join(DIRETORIO_BASE, 'logs')
DIRETORIO_IMAGENS = os.path.join(DIRETORIO_BASE, 'imagens')
DIRETORIO_MODELOS = os.path.join(DIRETORIO_BASE, 'modelos')

# Criação de diretórios se não existirem
os.makedirs(DIRETORIO_DADOS, exist_ok=True)
os.makedirs(DIRETORIO_LOGS, exist_ok=True)
os.makedirs(DIRETORIO_IMAGENS, exist_ok=True)
os.makedirs(DIRETORIO_MODELOS, exist_ok=True)

# Configurações de Scraping
URL_BASE_ZAP = "https://www.zapimoveis.com.br/venda/imoveis/pr+ponta-grossa"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"

# Configurações de Geocodificação
NOME_CIDADE = "Ponta Grossa"
NOME_ESTADO = "Parana"
NOME_PAIS = "Brazil"

# Configurações de Modelagem
SEED = 42
TAMANHO_TESTE = 0.2
FOLDS_VALIDACAO = 5
