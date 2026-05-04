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

# Importa o re para extrair o ID do produto da URL
import re

def extrair_id_produto(url):
    # Extrai o ID do produto da URL para usar como nome do arquivo de histórico
    id_produto = re.search(r"MLB-?\d+", url)
    if id_produto:
        return id_produto.group().replace("-", "")
    return "produto_desconhecido"

def buscar_preco(url, preco_alvo):
    # Extrai o ID do produto da URL
    id_produto = extrair_id_produto(url)

    # Configura o Firefox para rodar em modo invisível
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
        cupom = None

    # Fecha o navegador
    navegador.quit()

    # Cria um nome de arquivo baseado no nome do produto
    nome_arquivo = nome_produto[:30].strip().replace(" ", "_").replace("/", "")
    arquivo_historico = f"historico_{nome_arquivo}.json"

    # Verifica se já existe um histórico salvo para esse produto
    if os.path.exists(arquivo_historico):
        with open(arquivo_historico, "r", encoding="utf-8") as f:
            historico = json.load(f)
    else:
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

    # Salva o histórico atualizado
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

    # Exibe o menor preço já registrado
    menor_preco = min(historico, key=lambda x: x["preco"])
    print(f"\n🏆 Menor preço já registrado: R$ {menor_preco['preco']} em {menor_preco['data']}")

    # Verifica se atingiu o preço alvo
    if preco_atual <= preco_alvo:
        print(f"\n🎯 ALERTA! Preço atual R$ {preco_atual} está abaixo do seu alvo de R$ {preco_alvo}!")
    else:
        print(f"\n⏳ Preço alvo: R$ {preco_alvo} | Faltam R$ {preco_atual - preco_alvo} para atingir o alvo")

    print(f"{'='*50}\n")

# Pede o link do produto para o usuário
url = input("Cole o link do produto do Mercado Livre e aperte Enter: ")

# Pede o preço alvo
preco_alvo = int(input("Digite o preço alvo (ex: 300): R$ "))

# Chama a função
buscar_preco(url, preco_alvo)