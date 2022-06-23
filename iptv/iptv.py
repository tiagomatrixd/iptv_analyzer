import urllib.error
import urllib.request
from json import loads
from datetime import datetime
import telebot

class Iptv_analyzer():

#Função que faz o envio das listas para os canais no telegram.
#Mude a API do bot e põe o id do canal, lembrando que quando o canal é privado o sinal de menos e 100(-100) são adicionados no inicio do ID do canal. 
	def sendTelegram(self):
		try:
			self.bot = telebot.TeleBot(TOKEN_BOT)
			self.functionalLists = open('funciona.txt', 'r').read()
			if len(self.functionalLists) == 0:
				return 'Nenhuma lista encontrada'
			self.bot.send_message(IDGROUP, self.functionalLists, parse_mode='Markdown')
			self.bot.send_message(IDGROUP, self.functionalLists, parse_mode='Markdown')
			print('Listas Enviadas!')
		except:
			print('Error')

	def iptv(self, url, serve):
		try:
			self.response = urllib.request.urlopen(url.replace('get.php', 'player_api.php')).read().strip()
			data = loads(self.response)
		except ValueError:
			pass
		except NameError:
			pass
		except urllib.error.HTTPError as exception:
			pass
		except urllib.error.HTTPError as err:
			print(err)
		user = data['user_info']['username']
		password = data['user_info']['password']
		expiration = data['user_info']['exp_date']
		status = data['user_info']['status']
		account_active = data['user_info']['max_connections']
		account_use = data['user_info']['active_cons']
		auth = data['user_info']['auth']
		server = data['server_info']['url']
		port = data['server_info']['port']
		datatempo = int(expiration)
		local_time = datetime.fromtimestamp(datatempo)

		if status == 'Active':
				self.a = open("funciona.txt", 'a')
				self.a.write(f"\nServidor: {serve}\nUsuário: ```{user}```\nSenha: ```{password}```\nVencimento: {local_time.strftime('%d %B %Y')}\n")
				self.a.close()
				print(f'''\n================================='
Nome de Usuario: {user}
Senha: {password}
Data de expedição: {local_time.strftime('%d %B %Y')}
Contas Ativas: {account_use}
Conexões Maximas: {account_active}
Servidor: {serve}
Status: {status}\n''')