{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("I started by running a port scan.")}}

{{console("nmap -T5 -p- 10.10.56.250", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-23 19:18 CET
Warning: 10.10.10.245 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.10.245
Host is up (0.074s latency).
Not shown: 65104 closed tcp ports (reset), 428 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 fa:80:a9:b2:ca:3b:88:69:a4:28:9e:39:0d:27:d5:75 (RSA)
|   256 96:d8:f8:e3:e8:f7:71:36:c5:49:d5:9d:b6:a4:c9:0c (ECDSA)
|_  256 3f:d0:ff:91:eb:3b:f6:e1:9f:2e:8d:de:b3:de:b2:18 (ED25519)
80/tcp open  http    gunicorn
|_http-server-header: gunicorn
|_http-title: Security Dashboard")}}

{{text("We end up finding 3 open ports:")}}

{{list(['21 (FTP)', '22 (SSH)', '80 (HTTP)'])}}

{{text("I first tried to log in anonymously to the FTP, but it failed so I continued with the HTTP server.")}}

{{image("../../static/writeups/cap/images/000001.jpg")}}

{{text("It was some kind of dashboard. I started looking through it.")}}

{{text("Upon clicking on <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Security Snapshot</code> it would generate a downloadable <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.pcap</code> file.")}}

{{image("../../static/writeups/cap/images/000002.jpg")}}

{{text("Every time I clicked on that option the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/data/3</code> portion of the URL would increment by 1 and generate a new file.")}}

{{text("Since it started at 1, I immedietaly wondered what would happen if I changed it to 0.")}}

{{image("../../static/writeups/cap/images/000003.jpg")}}

{{text("It seemed to work, and there were a couple of packets captured. I downloaded that <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.pcap</code> file and opened it with <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>wireshark</code>.")}}

{{header("PCAP file", "pcap-file")}}

{{image("../../static/writeups/cap/images/000004.jpg")}}

{{text("I looked through the packets and ended up finding credentials used to login to the FTP server.")}}

{{image("../../static/writeups/cap/images/000005.jpg")}}

{{text("By logging in as the user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>nathan</code> and using the found password, I successfully accessed the FTP server.")}}

{{text("In there I found a flag, but nothing else. I assumed the credentials worked for the SSH as well.")}}

{{text("Logging with the same credentials via SSH worked.")}}

{{image("../../static/writeups/cap/images/000006.jpg")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Since I knew my user's password first thing I checked were his sudo privilages, but that didn't reveal anything.")}}

{{text("I downloaded <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>linpeas</code> onto the target machine and ran it.")}}

{{image("../../static/writeups/cap/images/000007.jpg")}}

{{text("It says that <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/usr/bin/python3.8</code> has the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cap_setuid</code> capability.")}}

{{text("A quick search about this capability and I found this.")}}

{{link("https://www.hackingarticles.in/linux-privilege-escalation-using-capabilities/", "https://www.hackingarticles.in/wp-includes/images/w-logo-blue-white-bg.png", "Linux Privilege Escalation using Capabilities")}}

{{text("Using the command from the article, I was able to become root.")}}

{{console("/usr/bin/python3.8 -c 'import os; os.setuid(0); os.system('/bin/bash')'")}}

{{image("../../static/writeups/cap/images/000008.jpg")}}

{{script()}}

