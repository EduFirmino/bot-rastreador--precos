# Importa o Selenium para controlar o navegador automaticamente
from selenium import webdriver

# Importa opções de configuração do Firefox
from selenium.webdriver.firefox.options import Options

# Importa ferramentas para encontrar elementos na página
from selenium.webdriver.common.by import By

# Importa espera inteligente (aguarda o elemento aparecer na tela)
from selenium.webdriver.support.ui import WebDriverWait

# Importa condição de espera (espera até o elemento estar visível)
from selenium.webdriver.support import expected_conditions as EC

# Importa o time para usar pausas no código
import time

# Importa o json para salvar o histórico de preços em arquivo
import json

# Importa o datetime para registrar a data e hora de cada consulta
from datetime import datetime

# Importa o os para verificar se o arquivo de histórico já existe
import os

def buscar_preco(url):
    # Configura o Firefox para rodar em modo invisível (sem abrir janela)
    opcoes = Options()
    opcoes.add_argument("--headless")

    # Abre o Firefox automaticamente
    navegador = webdriver.Firefox(options=opcoes)

    # Acessa a URL do produto
    navegador.get(url)

    # Aguarda 3 segundos para a página carregar completamente
    time.sleep(3)

    # Inicializa as variáveis
    preco_atual = None
    nome_produto = None
    cupom = None

    try:
        # Busca o nome do produto
        nome_produto = navegador.find_element(By.CLASS_NAME, "ui-pdp-title").text
    except:
        nome_produto = "Produto não identificado"

    try:
        # Busca o preço principal do produto
        preco = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-pdp-price__second-line .andes-money-amount__fraction"))
        )
        # Converte o preço para número inteiro
        preco_atual = int(preco.text.replace(".", ""))
    except:
        print("Preço não encontrado")
        navegador.quit()
        return

    try:
        # Tenta encontrar cupom de desconto na página
        cupom = navegador.find_element(By.CLASS_NAME, "ui-pdp-coupon__pill").text
    except:
        # Se não encontrar cupom, ignora
        cupom = None

    # Fecha o navegador
    navegador.quit()

    # Define o nome do arquivo de histórico baseado no link do produto
    arquivo_historico = "historico.json"

    # Verifica se já existe um histórico salvo
    if os.path.exists(arquivo_historico):
        # Se existe, carrega o histórico anterior
        with open(arquivo_historico, "r", encoding="utf-8") as f:
            historico = json.load(f)
    else:
        # Se não existe, cria um histórico vazio
        historico = []

    # Pega a data e hora atual
    agora = datetime.now().strftime("%d/%m/%Y %H:%M")

    # Cria o registro atual
    registro = {
        "data": agora,
        "preco": preco_atual
    }

    # Adiciona o registro ao histórico
    historico.append(registro)

    # Salva o histórico atualizado no arquivo
    with open(arquivo_historico, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=4)

    # Exibe as informações do produto
    print(f"\n{'='*50}")
    print(f"Produto: {nome_produto}")
    print(f"Preço atual: R$ {preco_atual}")
    print(f"Consultado em: {agora}")

    # Verifica se há cupom de desconto
    if cupom:
        print(f"Cupom disponível: {cupom}")
    else:
        print("Nenhum cupom encontrado")

    # Compara com o histórico se tiver mais de uma consulta
    if len(historico) > 1:
        preco_anterior = historico[-2]["preco"]
        data_anterior = historico[-2]["data"]

        if preco_atual < preco_anterior:
            print(f"\n✅ PREÇO CAIU! Era R$ {preco_anterior} em {data_anterior}")
        elif preco_atual > preco_anterior:
            print(f"\n⚠️ PREÇO SUBIU! Era R$ {preco_anterior} em {data_anterior}")
        else:
            print(f"\nPreço estável desde {data_anterior}")

    # Exibe o menor preço já registrado no histórico
    menor_preco = min(historico, key=lambda x: x["preco"])
    print(f"\n🏆 Menor preço já registrado: R$ {menor_preco['preco']} em {menor_preco['data']}")
    print(f"{'='*50}\n")

# Pede o link do produto para o usuário ao invés de deixar fixo no código
url = input("Cole o link do produto do Mercado Livre e aperte Enter: ")

# Chama a função passando a URL digitada pelo usuário
buscar_preco(url)