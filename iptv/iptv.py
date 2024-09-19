import urllib.error
import urllib.request
from json import loads
from datetime import datetime
import telebot
import logging

class IptvAnalyzer:
    def __init__(self, token_bot, id_group):
        self.bot = telebot.TeleBot(token_bot)
        self.id_group = id_group
        logging.basicConfig(filename='iptv_analyzer.log', level=logging.ERROR)

    def send_telegram(self):
        try:
            functional_lists = open('funciona.txt', 'r').read()
            if not functional_lists:
                return 'Nenhuma lista encontrada'
            self.bot.send_message(self.id_group, functional_lists, parse_mode='Markdown')
            print('Listas Enviadas!')
        except Exception as e:
            logging.error(f'Error sending message: {e}')
            print('Error sending message')

    def iptv(self, url, serve):
        try:
            response = urllib.request.urlopen(url.replace('get.php', 'player_api.php')).read().strip()
            data = loads(response)

            # Verificar se os dados contêm as chaves necessárias
            user_info = data.get('user_info', {})
            server_info = data.get('server_info', {})
            if not user_info or not server_info:
                logging.error(f'Invalid data received for URL: {url}')
                return

            user = user_info.get('username', 'N/A')
            password = user_info.get('password', 'N/A')
            expiration = user_info.get('exp_date', '0')
            status = user_info.get('status', 'Inactive')
            account_active = user_info.get('max_connections', 0)
            account_use = user_info.get('active_cons', 0)

            if status == 'Active':
                datatempo = int(expiration)
                local_time = datetime.fromtimestamp(datatempo)

                with open("funciona.txt", 'a') as a:
                    a.write(f"\nServidor: {serve}\nUsuário: ```{user}```\nSenha: ```{password}```\nVencimento: {local_time.strftime('%d %B %Y')}\n")

                print(f'''
=================================
Nome de Usuario: {user}
Senha: {password}
Data de expedição: {local_time.strftime('%d %B %Y')}
Contas Ativas: {account_use}
Conexões Maximas: {account_active}
Servidor: {serve}
Status: {status}
''')

        except urllib.error.HTTPError as e:
            logging.error(f'HTTP Error: {e.code} for URL: {url}')
        except ValueError:
            logging.error(f'Value Error while processing data for URL: {url}')
        except Exception as e:
            logging.error(f'Error: {e} for URL: {url}')

# Exemplo de uso:
# TOKEN_BOT = 'sua_token_aqui'
# IDGROUP = 'seu_id_aqui'
# iptv_analyzer = IptvAnalyzer(TOKEN_BOT, IDGROUP)
# iptv_analyzer.send_telegram()
