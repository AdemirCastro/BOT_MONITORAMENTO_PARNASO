import requests
import smtplib
import email.message
import pathlib
import logging
import warnings
import json
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
project_dir = str(pathlib.Path(__file__).parent.parent.resolve())
file_dir = str(pathlib.Path(__file__).parent.resolve())
load_dotenv(project_dir+'/config/config_file.env')
logging.basicConfig(filename=project_dir+'/log/critical.log', level=logging.CRITICAL)
warnings.filterwarnings(action='ignore', module ='bs4')

def ultimo_post_agendamento() -> (datetime,str):
    """ Coleta a data e o link do último post sobre agendamentos
    
    Parâmetros:
    -----------
    None

    Retorno:
    --------
    data_post: datetime
        Data do último post sobre agendamentos
    link_post: str
        Link do último post sobre agendamentos
    """

    url = 'https://www.icmbio.gov.br/parnaserradosorgaos/destaques.html'

    sucess = False
    while not sucess:
        try:
            response = requests.get(url)
            sucess = True
        except requests.ReadTimeout:
            sucess = False
            continue
        except requests.ConnectTimeout:
            sucess = False
            continue
        except requests.exceptions.ConnectionError:
            sucess = False
            continue

    html     = response.content
    soup     = BeautifulSoup(html, 'lxml')
    tabela   = soup.find('div',{'class':'blog_not'})
    posts    = tabela.find_all('div',{'class','items-row'})
    for post in posts:
        if 'AGENDAMENTO' in post.find('a').text.upper():
            ultimo_post = post
            break

    data_post = datetime.strptime(
        ultimo_post.find('span',{'class':'createdate'}).text.strip(), 
        r'%d/%m/%y'
        )
    link_post = 'https://www.icmbio.gov.br' + ultimo_post.find('a').get('href')
    return data_post, link_post

def conteudo_post(url: str) -> (str,str):
    """ Coleta o título e o conteúdo de um post no site do PARNASO

    Parâmetros:
    -----------
    url: str
        Link do post para leitura
    
    Retorno:
    --------
    titulo: str
        Título do post
    corpo: str
        Conteúdo do post
    """

    sucess = False
    while not sucess:
        try:
            response = requests.get(url)
            sucess = True
        except requests.ReadTimeout:
            sucess = False
            continue
        except requests.ConnectTimeout:
            sucess = False
            continue
        except requests.exceptions.ConnectionError:
            sucess = False
            continue

    html     = response.content
    soup     = BeautifulSoup(html, 'lxml')
    titulo = soup.find('h2',{'class':'contentheading_not'}).text.strip()
    corpo  = soup.find('div',{'class':'item-page_not'}).text
    return titulo, corpo

def enviar_email(login: str, senha: str, nome_remetente: str, destinatarios: str, assunto: str, 
            corpo: str, content_type: str='text', smtp_adrress: str='smtp.gmail.com: 587') -> None:
    """ Envia um email

    Parâmetros:
    -----------
    login: str
        Login da conta de email.
    senha: str
        Senha para utilizar a conta de email através de aplicação.
    nome_remete: str
        Nome do remetente que aparecerá no email.
    destinatários: str
        String com os emails destinatários separados por vírgula.
    assunto: str
        Assunto do email.
    corpo: str
        Conteúdo do email.
    content_type: str, default='text'
        Tipo de conteúdo para construção do email. Por exemplo, você pode passar um html.
    smtp_address: str, default='smtp.gmail.com: 587'
        Endereço e porta do servidor SMTP do serviço de emails utilizado.

    Retorno:
    --------
    None
    """
    msg = email.message.Message()
    msg['Subject'] = assunto
    msg['From']    = nome_remetente
    msg['To']      = destinatarios
    msg.add_header('Content-Type', content_type)
    msg.set_payload(corpo)
    
    s = smtplib.SMTP(smtp_adrress)
    s.starttls()

    s.login(login,senha)
    s.sendmail(msg['From'],[msg['To']],msg.as_string().encode('utf-8'))
    print('email enviado')

if __name__ == '__main__':

    print('MONITORANDO SITE!')
    ultima_data = datetime.strptime(
        json.load(open(file_dir+'/ultimo_post.json'))['data'], 
        r'%d/%m/%y'
        )

    intervalo_verificacao = 10 #minutos
    while True:
        data_post, link_post = ultimo_post_agendamento()
        if data_post > ultima_data:
            print('NOVO POST DE AGENDAMENTO ENCONTRADO!')
            titulo, corpo = conteudo_post(link_post)
            enviar_email(
            os.getenv('LOGIN'), 
            os.getenv('SENHA'),
            os.getenv('NOME_REMETENTE'),
            os.getenv('DESTINATARIOS'), 
            titulo,
            corpo
            )

            ultimo_post = {
                "data": data_post.strftime(r'%d/%m/%y') 
                }
            with open(file_dir+'/ultimo_post.json','w') as outfile:
                json.dump(ultimo_post, outfile)
            print('MONITORANDO SITE!')
        sleep(intervalo_verificacao*60)
    