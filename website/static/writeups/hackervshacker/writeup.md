{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start off by scanning all the ports.")}}

{{console("nmap -T5 -p- 10.10.36.37", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-12 23:43 CET
Warning: 10.10.36.37 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.36.37
Host is up (0.086s latency).
Not shown: 65209 closed tcp ports (reset), 324 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 9f:a6:01:53:92:3a:1d:ba:d7:18:18:5c:0d:8e:92:2c (RSA)
|   256 4b:60:dc:fb:92:a8:6f:fc:74:53:64:c1:8c:bd:de:7c (ECDSA)
|_  256 83:d4:9c:d0:90:36:ce:83:f7:c7:53:30:28:df:c3:d5 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: RecruitSec: Industry Leading Infosec Recruitment
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 264.11 seconds")}}

{{text("We discover only 2 open ports: ")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("We visit the website on port 80. It is a website for hiring best security consultants in order to stop coding vulnerabilities.")}}

{{image("../../static/writeups/hackervshacker/images/000001.jpg")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{text("There is a CV upload form at the bottom of the page which might prove useful. I checked the source code and saw that it sends data to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/upload.php</code> so I went there.")}}

{{text("By checking the source code of that endpoint, I got the code responsible for uploading a file.")}}

{{image("../../static/writeups/hackervshacker/images/000002.jpg")}}

{{text("This code checks if a file has <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.pdf</code> extension and if yes, it saves it in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/cvs</code> directory.")}}

{{text("Let's try to upload a reverse shell.")}}

{{text("I went to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code> and grabbed a PentestMonkey PHP shell. Saved it into a file named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>shell.pdf.php</code>.")}}

{{text("Then I uploaded it and went to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/cvs/shell.pdf.php</code> to see if it worked.")}}

{{image("../../static/writeups/hackervshacker/images/000003.jpg")}}

{{text("Seemed like it got uploaded successfully and now we could run commands using the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>?cmd=</code> parameter in the URL.")}}

{{text("After visiting <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code> again and getting a URL encoded PHP exec shell, I passed it as the parameter after setting upa listener.")}}

{{text("It worked and I got a connection.")}}

{{image("../../static/writeups/hackervshacker/images/000004.jpg")}}

{{header("Shell as lachlan", "shell-as-lachlan")}}

{{text("I started enumerating the system as <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>www-data</code>.")}}

{{text("With my permissions, I was able to access the home directory of user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>lachlan</code>.")}}

{{text("Not only was there a flag, but the contents of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.bash_history</code> have not been cleared.")}}

{{console("cat .bash_history", "./cve.sh
./cve-patch.sh
vi /etc/cron.d/persistence
echo -e '[REDACTED]' | passwd
ls -sf /dev/null /home/lachlan/.bash_history")}}

{{text("We now got user's <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>lachlan</code> password and can switch to him.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("We can also check the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/cron.d/persistence</code> file that was edited recently.")}}

{{console("cat /etc/cron.d/persistence", "PATH=/home/lachlan/bin:/bin:/usr/bin
# * * * * * root backup.sh
* * * * * root /bin/sleep 1  && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 11 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 21 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 31 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 41 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done
* * * * * root /bin/sleep 51 && for f in `/bin/ls /dev/pts`; do /usr/bin/echo nope > /dev/pts/$f && pkill -9 -t pts/$f; done")}}

{{text("What interests us the most is the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>PATH</code> variable. Since a path to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>pkill</code> is not specified, we can create our own pkill binary inside of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/home/lachlan/bin</code> and make it run commands for us.")}}

{{text("I created a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>pkill</code> file inside of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/home/lachlan/bin</code> and added a reverse shell to it. Remember to also make it executeable.")}}

{{image("../../static/writeups/hackervshacker/images/000005.jpg")}}

{{text("After setting up a listener, I became root.")}}

{{image("../../static/writeups/hackervshacker/images/000006.jpg")}}

{{script()}}