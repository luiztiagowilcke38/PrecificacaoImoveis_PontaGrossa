import logging
import os
from configuracao import DIRETORIO_LOGS

def configurar_logger(nome, arquivo_log, nivel=logging.INFO):
    """Função para configurar o logger."""
    formatador = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    
    manipulador_arquivo = logging.FileHandler(os.path.join(DIRETORIO_LOGS, arquivo_log))        
    manipulador_arquivo.setFormatter(formatador)

    logger = logging.getLogger(nome)
    logger.setLevel(nivel)
    logger.addHandler(manipulador_arquivo)

    # Adicionar manipulador de console
    manipulador_console = logging.StreamHandler()
    manipulador_console.setFormatter(formatador)
    logger.addHandler(manipulador_console)

    return logger

# Logger principal
logger_principal = configurar_logger('logger_principal', 'projeto.log')
