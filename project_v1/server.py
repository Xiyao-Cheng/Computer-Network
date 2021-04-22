#coding:utf-8
# student name: Xiyao Cheng
# student number: 14370907
# Date: Apr 13th
# Program Description:
# This program is to finish the project version1
# The main purpose is to build a chatroom.
# There are 4 main functions:
# 1. login: use account and password, the information is stored in users.txt
# 2. newuser: account should be less than 32 and password should between 4-8, and account is unique
# 3. send message: both to the server and the client, both broadcasts and one-to-one communication
# 4. logout: logout from the chatroom
# I use socket to build the network connection.
# Need at least 2 socket, server and client
# Build the connection between sockets:
# 1. build the socket of the server, bind the host and port, listen the client
# 2. the socket of client requests for connection
# 3. server answers the request

import socket
import select
import socketserver
import _thread

host = '127.0.0.1'
port = 10907
server_address = (host, port)

inputs = []
status = {} # clients status
user_name = {} # users names
maxnum = 3


#build and initial server socket
def serverInit():
	print('My chat room server. Verison One.')
	soc = socket.socket()
	soc.bind(server_address)
	soc.listen(5)
	return soc

#build a new socket connection
def newConnection(soc):
	client, client_address = soc.accept()
	if len(inputs) > maxnum:
		try:
			inputs.append(client)
			user_name[client] = client_address
			status[client] = 'No'
			client.send(bytes('Sorry, the chatroom is full, maybe you can try again later.', encoding='utf-8'))
			inputs.remove(client)
		except Exception as e:
			pass
	else:
		try:
			client.send(bytes('My chat room client. Version One.', encoding ='utf-8'))
			inputs.append(client)
			user_name[client] = client_address
			status[client] = 'No'
		except Exception as e:
			print(e)

def run():
	soc = serverInit()
	inputs.append(soc)
	while True:
		readlist, writelist, errorlist = select.select(inputs, [], [])
		if len(readlist) == 0:
			print('Timeout...')
			soc.close()
			break
		for r in readlist:
			if r is soc:
				newConnection(soc)
			else:
				disconnect = False
				try:
					data = str(r.recv(1024))
				except socket.error:
					disconnect = True

				if disconnect:
					inputs.remove(r)
					for last in inputs:
						if last != soc and last != r:
							try:
								last.send(bytes(data,encoding = 'utf-8'))
							except Exception as e:
								print(e)
							else:
								pass
					print(str(user_name[r]) + ' disconnected.')
					del user_name[r]
				else:
					if isinstance(user_name[r], tuple):
						pass
					else:
						pass
				try:
					if 'login' in data or 'newuser' in data or 'send' in data or 'logout' in data:
						data_strings = data.replace('b\'','').replace('\'','').split(' ')
						if data_strings[0] == 'login':
							try:
								login(data_strings[1:], r)
							except Exception as e:
								r.send(bytes('Invalid commend!', encoding='utf-8'))
						elif data_strings[0] == 'newuser':
							try:
								newuser(data_strings[1:], r)
							except Exception as e:
								r.send(bytes('Invalid commend!', encoding='utf-8'))
						elif data_strings[0] == 'logout':
							logout(r)
						elif data_strings[0] == 'send':
							try:
								to(data_strings[1:], r)
							except Exception as e:
								r.send(bytes('Invalid commend!', encoding='utf-8'))
						else:
							r.send(bytes('Invalid commend', encoding = 'utf-8'))
					else:
						r.send(bytes('Invalid commend', encoding = 'utf-8'))
				except Exception as e:
					print(e)
	soc.close()


#user login function
def login(inf, client):
	infofile = open('users.txt')
	response = ''
	try:
		user = inf[0]
		pwd = inf[1]
		signal = 0
		for line in infofile:
			strs2 = line.replace('(','').replace(')','').replace('\n','').split(', ')
			account = strs2[0]
			password = strs2[1]
			if account == user and password == pwd:
				response = 'login confirmed'
				user_name[client] = account
				status[client] = 'Yes'
				client.send(bytes(response, encoding = 'utf-8'))
				print(user_name[client] + ' login.')
				signal = 1
				break
		if signal == 0:
			response = 'Denied. User name or password incorrect.'
			client.send(bytes(response, encoding = 'utf-8'))
	finally:
		infofile.close()

#create a new user.
def newuser(inf, client):
	infofile = open('users.txt')
	response = ''
	try:
		flag = 0
		acc = inf[0]
		for line in infofile:
			strs2 = line.replace('(','').replace(')','').split(', ')
			account = strs2[0]
			if account == acc:
				flag = 1
	finally:
		if flag == 0:
			if len(inf[0]) > 0 and len(inf[0]) < 32 and 4 <= len(inf[1]) and len(inf[1]) <= 8:
				winfo = open('users.txt', 'a')
				winfo.write('(' + inf[0] + ', ' + inf[1] + ')' + '\n')
				winfo.close()
				response = 'New user account created. Please login.'
				print('New user account created.')
			else:
				response = 'The format of the account or password is wrong!'
		else:
			response = 'Denied. User account already exists.'
		infofile.close()
		client.send(bytes(response, encoding = 'utf-8'))

# user logout
def logout(client):
	if status[client] == 'No':
		response = 'Denied. Please login first.'
		client.send(bytes(response, encoding = 'utf-8'))
	else:
		response = user_name[client] + ' left.'
		client.send(bytes(response, encoding = 'utf-8'))
		print(user_name[client] + ' logout.')
		del user_name[client]
		del status[client]
		inputs.remove(client)
		client.close()

# users send message to server
def to(inf, client):
	if status[client] == 'No':
		response = 'Denied. Please login first.'
		client.send(bytes(response, encoding = 'utf-8'))
	else:
		try:
			response = user_name[client] + ': ' + inf[0]
			client.send(bytes(response, encoding = 'utf-8'))
			print(user_name[client] + ': ' + inf[0])
		except Exception as e:
			print(e)



if __name__ == '__main__':
	run()