#coding: utf-8

import socket
import thread
import sys
import os

def existe_arquivo(arquivo):  # Verifica se o arquivo solicitado existe
	caminho = pastaserv + '/' + arquivo
	return os.path.isfile(caminho)
	
def conectado(con, cliente):
	print "Conectado ao cliente ", cliente
	
	mensagem = con.recv(1024)
	
	arquivo = mensagem.split(' ')
	
	arqsolicitado = arquivo[1]
	print arqsolicitado
	if existe_arquivo(arqsolicitado):
		f = open(pastaserv + arqsolicitado)
		cabecalho = 'HTTP/1.0 200 OK\r\nConnection: keep-alive\r\nExpires: -1\r\n\r\n'
		arq = f.read()
		envia = cabecalho + arq
		con.sendall(envia)
		con.close()
	else:
		cabecalho = 'HTTP/1.0 404 Not Found\r\nExpires: -1\r\n\n'
		envia = '404 Not Found'
		con.send(envia)
		con.close()
	print "Fechando conexao com o cliente ", cliente

HOST = 'localhost' 		# Endereco do servidor
PORT = 8800 			# Porta padrao caso nao seja especificada nos parametros

if len(sys.argv) == 1:  # Verifica se o usuario passou pelo menos o parametro obrigatorio
	print "Nenhuma pasta passada por parametro!\nEncerrando servidor...\n"
	sys.exit()

if len(sys.argv) == 3:  # Verifica se o usuario especificou a porta
	PORT = int(sys.argv[2])

pastaserv = sys.argv[1]

socketserv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketserv.bind((HOST, PORT)) 	# associa o socket a uma porta e um IP
socketserv.listen(1)			# coloca o servidor escutando (modo passivo)
print("Servidor iniciado no endereço: http://%s porta: %d" %(HOST, PORT))

while True:
	con, cliente = socketserv.accept() # retorna um objeto socket novo e o endereço do cliente
	thread.start_new_thread(conectado, tuple([con, cliente])) # inicia a thread para retornar o arquivo solicitado pelo cliente
socketserv.close()