# -*- coding: UTF-8 -*-
from socket import *

HOST = 'viphk.ngrok.org'
PORT = 10054
BUFSIZ = 1024
ADDR = (HOST,PORT)

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    data = input('>')
    data = data.encode('UTF-8')
    tcpCliSock.send(data)
    clirecv = tcpCliSock.recv(BUFSIZ)
    print (clirecv.decode('utf-8'))
tcpCliSock.close()
