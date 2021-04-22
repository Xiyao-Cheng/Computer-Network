#coding:utf-8
#This is a program which builds a chatroom. Server and clients can communicate with each other.
#This is the .py file for client end.
#Author: Xiyao Cheng, student number:14370907
#Date:04/13/2021

import sys
import socket
import select
import threading
import time

host = '127.0.0.1'
port = 10907

address = (host, port)

# Build connect
def connect():
	soc = socket.socket()
	soc.connect(address)
	return soc

# listen from server
def listen(soc):
	my = [soc]
	while True:
		read, write, error = select.select(my, [], [])
		if soc in read:
			try:
				message = str(soc.recv(1024))
				end = len(message)-1
				message = message[2:end]
				if message != '':
					print(message)
				if 'Logout success' in message:
					print('Connection have been break!')
					break
			except socket.error:
				print('Socket is error!')
				soc.close()
				break
	soc.close()
	exit()

#send message to server
def talk(soc):
	while True:
		try:
			info = input()
		except Exception as e:
			print('can\'t input')
			exit()

		try:
			soc.send(bytes(info, encoding='utf-8'))
		except Exception as e:
			print(e)
			exit()


if __name__ == '__main__':
	ss = connect()
	thread = threading.Thread(target=listen, args=(ss,))
	thread.start()
	thread1 = threading.Thread(target=talk, args=(ss,))
	thread1.start()
