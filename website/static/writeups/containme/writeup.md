{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{text("<code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>THIS ROOM IS BROKEN AND CANNOT BE COMPLETED. I STILL LEFT IT FOR THE WEB EXPLOITATION PART.</code>")}}

{{header("Enumeration", "enumeration")}}

{{text("We run a port scan.")}}

{{console("nmap -T5 -p- 10.10.200.176", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-17 19:50 CET
Warning: 10.10.0.160 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.0.160
Host is up (0.12s latency).
Not shown: 65292 closed tcp ports (reset), 239 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
22/tcp   open  ssh           OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 a6:3e:80:d9:b0:98:fd:7e:09:6d:34:12:f9:15:8a:18 (RSA)
|   256 ec:5f:8a:1d:59:b3:59:2f:49:ef:fb:f4:4a:d0:1d:7a (ECDSA)
|_  256 b1:4a:22:dc:7f:60:e4:fc:08:0c:55:4f:e4:15:e0:fa (ED25519)
80/tcp   open  http          Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
2222/tcp open  EtherNetIP-1?
|_ssh-hostkey: ERROR: Script execution failed (use -d to debug)
8022/tcp open  ssh           OpenSSH 7.7p1 Ubuntu 4ppa1+obfuscated (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 dc:ae:ea:27:3f:ab:10:ae:8c:2e:b3:0c:5b:d5:42:bc (RSA)
|   256 67:29:75:04:74:1b:83:d3:c8:de:6d:65:fe:e6:07:35 (ECDSA)
|_  256 7f:7e:89:c4:e0:a0:da:92:6e:a6:70:45:fc:43:23:84 (ED25519)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 711.14 seconds")}}

{{list(['22 (SSH)', '80 (HTTP)', '2222 (EtherNetIP-1)', '8022 (SSH)'])}}

{{text("Let's begin by checking out the web page.")}}

{{image("../../static/writeups/containme/images/000001.jpg")}}

{{header("Getting reverse shell", "getting-reverse-shell")}}

{{text("We find a default Apache installation page.")}}

{{text("I continued with directory enumerating, but couldn't find anything until I added <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>php</code> as a extension.")}}

{{console("gobuster dir -u http://10.10.0.160 -w /usr/share/wordlists/dirb/big.txt -x php", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.0.160
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Extensions:              php
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 276]
/.htaccess.php        (Status: 403) [Size: 276]
/.htpasswd            (Status: 403) [Size: 276]
/.htpasswd.php        (Status: 403) [Size: 276]
/index.php            (Status: 200) [Size: 329]
/info.php             (Status: 200) [Size: 68921]
Progress: 40938 / 40940 (100.00%)
===============================================================
Finished
===============================================================")}}

{{text("Looking through the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/info.php</code> page, I couldn't find anything interesting besides a hostname so I continued with <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/index.php</code>.")}}

{{text("Glancing at the page source code we find what is probably a hint.")}}

{{image("../../static/writeups/containme/images/000002.jpg")}}

{{text("After getting stuck for a while, I found the next step.")}}

{{text("The <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>path</code> refers to a URL parameter.")}}

{{image("../../static/writeups/containme/images/000003.jpg")}}

{{text("Let's see if we can leverage this to gain a reverse shell.")}}

{{text("In order to run a command we need to add <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.;</code> before the command.")}}

{{text("The <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.</code> resolves to the current directory and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>;</code> acts as a command seperator, allowing the command we pass to execute.")}}

{{text("We proceed to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code> and get a PHP exec shell, URL encode it and pass it as the argument.")}}

{{image("../../static/writeups/containme/images/000004.jpg")}}

{{text("It works successfuly, and we have a reverse shell.")}}

{{header("Flag?", "flag")}}

{{text("In the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/home/mike</code> directory we find a binary named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>1cryptupx</code>.")}}

{{text("It only seems to print out a banner and nothing more.")}}

{{text("While checking for binaries with SUID set, I came across some interesting files.")}}

{{console("find / -perm -4000 2>/dev/null", "/usr/share/man/zh_TW/crypt
/usr/bin/newuidmap
/usr/bin/newgidmap
/usr/bin/passwd
/usr/bin/chfn
/usr/bin/at
/usr/bin/chsh
/usr/bin/newgrp
/usr/bin/sudo
/usr/bin/gpasswd
...")}}

{{text("The <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/usr/share/man/zh_TW/crypt</code> binary seemed to do the same thing as the previous one.")}}

{{text("I tried running it with some random parameters and when I passed user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>mike</code>, it gave me root.")}}

{{image("../../static/writeups/containme/images/000005.jpg")}}

{{text("But the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/root</code> directory was empty and the flag was nowhere to be found?")}}

{{text("Running out of ideas, I tried logging in as user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>mike</code> since I now had access to his <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id_rsa</code> key. That didn't work.")}}

{{text("I didn't have a clue what to do so I checked the room solution.")}}

{{image("../../static/writeups/containme/images/000006.jpg")}}

{{text("Great. So we can't actually complete this room.")}}

{{text(":(")}}

{{script()}}