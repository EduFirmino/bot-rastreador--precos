# Bot Rastreador de Preços 🤖

Bot desenvolvido em Python que rastreia o preço de produtos do Mercado Livre e notifica quando há variações de preço.

## Funcionalidades
- Busca o preço atual de qualquer produto do Mercado Livre
- Detecta cupons de desconto disponíveis
- Salva histórico de preços com data e hora
- Compara preço atual com consultas anteriores
- Alerta quando o preço sobe ou cai
- Define um preço alvo e avisa quando o produto atingir esse valor
- Histórico separado por produto

## Tecnologias utilizadas
- Python 3
- Selenium
- Firefox (WebDriver)

## Como usar
1. Instale as dependências: `pip install selenium`
2. Execute o arquivo Bot.py
3. Cole o link do produto do Mercado Livre
4. Digite o preço alvo desejado
5. O bot retorna o preço atual, histórico e alertas

## Versões
- v1.0 - Busca de preço básica
- v1.1 - Histórico de preços, detecção de cupom e input do usuário
- v1.2 - Histórico separado por produto e gitignore
