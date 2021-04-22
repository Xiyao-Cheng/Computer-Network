#coding:utf-8

import sys
import socket
import select
import threading

host = '127.0.0.1'
port = 10907

address = (host, port)

def connect():
	soc = socket.socket()
	soc.connect(address)
	return soc

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

def talk(soc):
	while True:
		try:
			info = input()
		except Exception as e:
			print('can\'t input')
			exit()

		try:
			soc.send(bytes(info, encoding='utf-8'))
			if info == 'logout':
				sys.exit(1)
		except Exception as e:
			print(e)
			exit()


if __name__ == '__main__':
	ss = connect()
	thread = threading.Thread(target=listen, args=(ss,))
	thread.start()
	thread1 = threading.Thread(target=talk, args=(ss,))
	thread1.start()
