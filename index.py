from datetime import datetime
import os
from tempfile import NamedTemporaryFile
from zipfile import ZipFile
import requests
from bs4 import BeautifulSoup

def isValidAnexo(title, numeros):
    return any(f'Anexo {numero}' in title for numero in numeros)


def writeTempFile(bytes):
    file = NamedTemporaryFile(delete=False)
    file.write(bytes)
    file.close()
    return file.name


def baixarAnexos(url, numeros):
    print('Buscando dados da página web...')
    result = requests.get(url).text

    print('Fazendo parse dos dados...')
    soup = BeautifulSoup(result, 'html.parser')

    date = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')

    print('Iniciando a criação do arquivo zip...')
    zip_name = f'Anexos_{"_".join(numeros)}_Rol_Procedimentos_Eventos_Saúde_{date}.zip'
    zip_path = os.path.join(os.getcwd(), zip_name)

    with ZipFile(zip_path, 'w') as zip:
        for tag in soup.find_all('a'):
            text = str(tag.string)
            if isValidAnexo(text, numeros):
                href = tag.get('href')
                file_name = os.path.basename(href)
                temp_name = writeTempFile(requests.get(href).content)
                print(f'Adicionando o arquivo "{file_name}" ao zip...')
                zip.write(temp_name, file_name)
                os.unlink(temp_name)
    print(f'Arquivo salvo em: "{zip_path}"')


baixarAnexos(
    url='https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude',
    numeros=['I', 'II', 'III', 'IV']
)
