import requests
from bs4 import BeautifulSoup

url = 'https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

numeros = ['I', 'II', 'III', 'IV']

for tag in soup.find_all('a'):
    text = str(tag.string)
    if any(f'Anexo {numero}' in text for numero in numeros):
        href = tag.get('href')
        print(f'text: {text}')
        print(f'href: {href}\n')
