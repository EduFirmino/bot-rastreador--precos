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

    try:
        # Busca o preço principal do produto especificamente
        preco = WebDriverWait(navegador, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".ui-pdp-price__second-line .andes-money-amount__fraction"))
        )

        # Imprime o preço encontrado
        print(f"Preço atual: R$ {preco.text}")

    except:
        # Se não encontrar o preço, avisa o usuário
        print("Preço não encontrado")

    # Fecha o navegador
    navegador.quit()

# URL do produto que queremos rastrear
url = "https://produto.mercadolivre.com.br/MLB-5159817272-tnis-fila-venture-tracer-lite-masculino-casual-original-_JM"

# Chama a função
buscar_preco(url)