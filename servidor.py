#coding: utf-8

import socket
import thread
import sys
import os

HOST = 'localhost' 		# endereco ip do servidor
PORT = 6666 			# porta que o servidor esta

if len(sys.argv) == 1:
	print "Nenhuma pasta passada por parametro!\nEncerrando servidor...\n"

if len(sys.argv) == 3:
	PORT = int(sys.argv[2])

pastaserv = sys.argv[1]

def existe_arquivo(arquivo):
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
		cabecalho = 'HTTP/1.0 200 OK\r\nExpires: -1\r\n \n'
		arq = f.read()
		envia = cabecalho + arq
		con.sendall(envia)
		con.close()
	else:
		con.send("Erro 404 - Arquivo nao encontrado")
		con.close()
	print "Fechando conexao com o cliente ", cliente


tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind((HOST, PORT)) 	# associa o socket a uma porta e um IP
tcp.listen(1)			# coloca o servidor escutando (modo passivo)
print("Servidor iniciado no endereço: http://%s porta: %d" %(HOST, PORT))

while True:
	con, cliente = tcp.accept() # retorna um objeto socket novo e o endereço do cliente
	thread.start_new_thread(conectado, tuple([con, cliente]))
tcp.close()
