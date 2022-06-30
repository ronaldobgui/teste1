from datetime import datetime
import os
import re
from tempfile import NamedTemporaryFile
from zipfile import ZipFile
from cv2 import exp
import requests
from bs4 import BeautifulSoup


def writeTempFile(bytes):
    with NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(bytes)
        return temp_file.name


class AnexoReference:
    def __init__(self, file_name, temp_name):
        self.file_name = file_name
        self.temp_name = temp_name


def baixarAnexos(url, numeros):
    print('Buscando dados da página web...')
    try:
        if len(numeros) == 0:
            raise Exception('Nenhum anexo foi definido para download...')

        result = requests.get(url).text

        # fazendo parse dos dados
        soup = BeautifulSoup(result, 'html.parser')

        regex_anexo = re.compile(f'anexo ({"|".join(numeros)})', re.IGNORECASE)
        tags_anexo = soup.find_all('a', string=regex_anexo)

        refs_anexo = []

        # baixando anexos
        for tag_anexo in tags_anexo:
            href = tag_anexo.get('href')
            file_name = os.path.basename(href)
            print(f'Baixando o anexo "{file_name}"...')

            try:
                reference = AnexoReference(
                    file_name=file_name,
                    temp_name=writeTempFile(requests.get(href).content),
                )
                refs_anexo.append(reference)

            except requests.RequestException:
                print(f'Erro ao baixar anexo {file_name} (ignorando...)')

            except Exception:
                print(f'Erro ao salvar anexo {file_name} (ignorando...)')

        if len(tags_anexo) == 0:
            raise Exception('Nenhum anexo foi encontrado...')

        date = datetime.now().strftime('%d_%m_%Y_%H_%M_%S')

        print('Iniciando a criação do arquivo zip...')
        zip_name = f'Anexos_{"_".join(numeros)}_Rol_Procedimentos_Eventos_Saúde_{date}.zip'
        zip_path = os.path.join(os.getcwd(), zip_name)

        try:
            with ZipFile(zip_path, 'w') as zip:
                for ref in refs_anexo:
                    zip.write(ref.temp_name, ref.file_name)
        except:
            if(os.path.exists(zip_path)):
                os.unlink(zip_path)

            raise Exception('Erro ao salvar arquivo zip...')

        print(f'Deletando arquivos temporários...')
        for ref in refs_anexo:
            if(os.path.exists(zip_path)):
                os.unlink(ref.temp_name)

        print(f'Arquivo salvo em: "{zip_path}"')

    except requests.RequestException:
        print('Houve um problema ao recuperar os dado da página web...')

    except Exception as e:
        print(f'Erro: {e}')


baixarAnexos(
    url='https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude',
    numeros=['I', 'II', 'III', 'IV']
)
