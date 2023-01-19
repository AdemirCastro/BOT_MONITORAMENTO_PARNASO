
# BOT DE MONITORAMENTO DO AGENDAMENTO NO PARNASO
Esse programa monitora o site do PARNASO e envia um email quando surge um novo post sobre agnedamentos.


## Requisitos
O programa deve ser executado em Python3. Todos os requisitos estão listados no arquivo [/requirements.txt]().  
Para instalar todos de uma só vez, basta executar o programa:
```bash
sudo pip3 install -r requirements.txt
```
na pasta do projeto.
## Configuration
As configurações do email do email são feitas através do arquivo [/config/config_file.env]().  
As variáveis são:  
- LOGIN: loging do usuário em um serviço de emails
- SENHA: senha para login por aplicações na conta de emails utilizada
- REMETENTE: nome do remetente que aparecerá no email enviado
- DESTINATARIOS: emails dos destinatários separados por vírgulas em uma string.
## Execution
O arquivo [/src/monitoramento.py]() contém todas as funções do projeto, e também faz o monitoramento quando é executado pela main.  
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Feedback

Se quiser enviar algum feedback, basta enviar um email para oademircastro@gmail.com.