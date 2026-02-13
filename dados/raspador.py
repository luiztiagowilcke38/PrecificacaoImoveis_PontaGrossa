from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random
import os
import sys

# Adiciona o diretório raiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from configuracao import DIRETORIO_DADOS

# URL OLX Ponta Grossa (Filtro: Venda de Apartamentos/Casas)
URL_OLX = "https://www.olx.com.br/imoveis/venda/estado-pr/regiao-de-ponta-grossa-e-guarapuava/ponta-grossa"

def extrair_dados_olx(page):
    """Extrai dados dos cards da OLX."""
    dados_pagina = []
    
    # Seletores da OLX (podem mudar, baseados no padrão atual)
    # Cards geralmente são 'li' dentro de uma lista ou divs com classe específica
    # Vamos buscar por links que parecem ser anúncios
    
    # Espera carregar a lista
    try:
        # Tenta seletor genérico de lista de anúncios
        page.wait_for_selector('ul#ad-list li, div[data-ds-component="DS-AdCard"]', timeout=15000)
    except:
        print("  - Timeout esperando lista de anúncios (pode ser captcha ou layout diferente).")
        # Tira screenshot para debug se possível (mas aqui só printamos)
        return []

    # Tenta pegar todos os links que parecem ser de anúncios
    cards = page.locator('a[data-ds-component="DS-NewAdCard-Link"]').all()
    
    if not cards:
        print("  - Seletor A falhou. Tentando seletor B...")
        cards = page.locator('ul#ad-list li a').all()

    print(f"  - Encontrados {len(cards)} cards potenciais.")

    for i, card in enumerate(cards):
        try:
            # Texto completo do card para parsing robusto
            texto_completo = card.inner_text()
            # print(f"DEBUG Card {i}: {texto_completo[:50]}...")

            titulo = "Imóvel sem título"
            try:
                titulo = card.locator('h2').first.inner_text(timeout=100)
            except: pass

            preco = "0"
            try:
                # Busca preço no texto do card se seletor falhar
                if "R$" in texto_completo:
                    import re
                    match = re.search(r'R\$\s?([\d.]+)', texto_completo)
                    if match:
                        preco = match.group(1).replace('.', '')
            except: pass
            
            detalhes = texto_completo
            
            area = "0"
            quartos = "0"
            
            # Parsing de string "2 quartos | 50m² | 1 vaga"
            if "m²" in detalhes:
                import re
                match_area = re.search(r'(\d+)\s?m²', detalhes)
                if match_area: area = match_area.group(1)
            
            if "quarto" in detalhes:
                import re
                match_quartos = re.search(r'(\d+)\s?quarto', detalhes)
                if match_quartos: quartos = match_quartos.group(1)

            endereco = "Ponta Grossa, PR"
            # Tenta achar bairro
            if " - " in titulo:
                # Ex: "Apartamento em Oficinas - ..."
                partes = titulo.split(' - ')
                if len(partes) > 1:
                    endereco = partes[0]

            banheiros = "1"
            vagas = "0"
            if "vaga" in detalhes:
                import re
                match_vaga = re.search(r'(\d+)\s?vaga', detalhes)
                if match_vaga: vagas = match_vaga.group(1)

            dados_pagina.append({
                "titulo": titulo,
                "endereco": endereco,
                "preco": preco,
                "area": area,
                "quartos": quartos,
                "banheiros": banheiros,
                "vagas": vagas
            })
        except Exception as e:
            # print(f"Erro card {i}: {e}")
            continue
            
    return dados_pagina

def executar_raspagem_olx(num_paginas=20):
    """Executa o scraper na OLX."""
    print(f"Iniciando coleta OLX Ponta Grossa (Alvo: {num_paginas} páginas)...")
    
    todos_dados = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) # Headless True para ser rápido, OLX bloqueia menos
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        page = context.new_page()

        for i in range(1, num_paginas + 1):
            url = f"{URL_OLX}?o={i}"
            print(f"Navegando para página {i}...", end='\r')
            
            try:
                page.goto(url, timeout=60000, wait_until='domcontentloaded')
                
                # Scroll para garantir carregamento
                page.mouse.wheel(0, 500)
                time.sleep(1)
                page.mouse.wheel(0, 1000)
                time.sleep(1)

                dados = extrair_dados_olx(page)
                if dados:
                    print(f"  - Extraídos {len(dados)} imóveis.")
                    todos_dados.extend(dados)
                
                time.sleep(random.uniform(2, 5))

            except Exception as e:
                print(f"\nErro na página {i}: {e}")

        browser.close()

    print("\n")
    if todos_dados:
        df = pd.DataFrame(todos_dados)
        
        # Limpeza básica imediata
        df = df[df['preco'] != "0"]
        df.drop_duplicates(inplace=True)
        
        caminho_csv = os.path.join(DIRETORIO_DADOS, 'dados_brutos.csv')
        df.to_csv(caminho_csv, index=False)
        print(f"Coleta OLX Finalizada! {len(df)} imóveis salvos.")
    else:
        print("Nenhum dado coletado da OLX.")

if __name__ == "__main__":
    executar_raspagem_olx()
