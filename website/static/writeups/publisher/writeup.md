{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start by scanning the ports.")}}

{{console("nmap -T5 -p- 10.10.125.236", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-04 16:39 CET
Nmap scan report for 10.10.125.236
Host is up (0.076s latency).
Not shown: 56415 closed tcp ports (conn-refused), 9118 filtered tcp ports (no-response)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 440.36 seconds
")}}

{{text("We discover 2 open ports: ")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("We visit port 80 and get back a blog like site about <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SPIP</code>.")}}

{{image("../../static/writeups/publisher/images/000001.jpg")}}

{{text("I couldn't find anything interesting in the source code so I proceeded with directory scanning.")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{console("gobuster dir -u http://10.10.125.236 -w /usr/share/wordlists/dirb/big.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.125.236
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/images               (Status: 301) [Size: 315] [--> http://10.10.125.236/images/]
/server-status        (Status: 403) [Size: 278]
/spip                 (Status: 301) [Size: 313] [--> http://10.10.125.236/spip/]
Progress: 20469 / 20470 (100.00%)
===============================================================
Finished
===============================================================")}}

{{text("We find <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>spip</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>images</code> directories. The  first one looked more interesting so that's what I focused on.")}}

{{text("I was able to find the version of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SPIP</code> that is being run.")}}

{{image("../../static/writeups/publisher/images/000002.jpg")}}

{{text("Now we are able to search for a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SPIP 4.2.0 exploit</code>. We come across this using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>metasploit</code>.")}}

{{image("../../static/writeups/publisher/images/000003.jpg")}}

{{text("We set correct parameters and run the exploit. We should get a reverse shell.")}}

{{image("../../static/writeups/publisher/images/000004.jpg")}}

{{header("Last flag", "last-flag")}}

{{text("We now can go to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/home/think/.ssh</code> directory and copy <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id_rsa</code> onto our machine and log in via SSH for easier access.")}}

{{text("When searching for files with SUID bits I noticed something unusual.")}}

{{console("find / -perm -4000 2>/dev/null", "/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/xorg/Xorg.wrap
/usr/sbin/pppd
/usr/sbin/run_container
/usr/bin/at
/usr/bin/fusermount
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/sudo
/usr/bin/chsh
/usr/bin/passwd
/usr/bin/mount
/usr/bin/su
/usr/bin/newgrp
/usr/bin/pkexec
/usr/bin/umount")}}

{{text("The <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>run_container</code> binary was something unusual. I used the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>strings</code> command on it and tried to extract anything useful from it.")}}

{{image("../../static/writeups/publisher/images/000005.jpg")}}

{{text("I noticed this binary uses the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>run_container.sh</code> file in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt</code> directory.")}}

{{text("I tried to get to that file but to my surprise I got a 'permissions denied' error when trying to go to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt</code> directory.")}}

{{text("This was happening because of the App Armor which is a tool to restrict certain things by defining rules.")}}

{{text("We are able to find a file defining the rule preventing us from going to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt</code>.")}}

{{image("../../static/writeups/publisher/images/000006.jpg")}}

{{text("But according to this our shell should be <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ash</code> and not our current <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/think</code>, right?")}}

{{text("I copied <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/bin/bash</code> to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/dev/shm</code> and run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/dev/shm/bash -p</code> to change my shell so I can edit files in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt</code>.")}}

{{text("Thanks to that I was able to edit the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt/run_container.sh</code> file so that it runs a shell as root and I will be able to read the last flag.")}}

{{image("../../static/writeups/publisher/images/000007.jpg")}}

{{script()}}