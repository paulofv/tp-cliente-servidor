#coding: utf-8

import sys
import socket
import os

PORT = 80 #porta padrão caso usuário não especifique

if len(sys.argv) == 1:
    print "Nao foi informado a url no paramentro!\n"
    sys.exit()
    
if len(sys.argv) == 3:
	PORT = int(sys.argv[2])
	
link = sys.argv[1].replace("https://", "").replace("http://", "") #remover http:// do link

HOST = link.split('/') #separar o host do resto da url
HOST = HOST[0]

socketnav = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketnav.connect((HOST, PORT))

print "Conectando a " + HOST + "\n\n"

url = link.split('/')

nomearq = ''

if len(url) > 1:
	nomearq = url[len(url)-1] #recebe o nome do arquivo caso seja especificado
	
del url[0]
caminho = ''

if type(url) == list:
	for i in url:
		caminho += '/' + i #monta o caminho para ser feita a requisicao
else:
	caminho = '/'
	
if len(nomearq) == 0:
	nomearq = "index.html"

requisicao = 'GET '+ caminho + ' HTTP/1.0\r\nHost: ' + HOST + '\r\n\r\n'
socketnav.sendall(requisicao)

pagina = ''

while (True):
	rcv = socketnav.recv(4096)
	if not rcv:
		break
	pagina += rcv

linhas = pagina.split('\n'); #separa o conteudo recebido em linhas

i = 0
while(True):  #separa o cabecalho da Cabeçalho HTTP do conteudo
	if len(linhas[i]) == 1:
		inicio = i + 1
		break
	i += 1

dir = './' + HOST #pasta pra salvar o conteudo
if not os.path.isdir(dir): #verifica se ja existe, se nao existe cria
	os.makedirs(dir)

arqsaida = dir + '/' + nomearq

arquivo_saida = open(arqsaida,"w") #criando arquivo de saida
	
i = 0
print "Cabeçalho HTTP"
while(i < inicio):  #imprimindo o Cabeçalho HTTP na tela
	print(linhas[i])
	i += 1
	
while (inicio < len(linhas)):  #salvando o conteudo no arquivo
	arquivo_saida.write(linhas[inicio])
	arquivo_saida.write("\n")
	inicio += 1

socketnav.close