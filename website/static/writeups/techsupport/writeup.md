{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We begin with port scanning.")}}

{{console("nmap -T5 -p- -sC -sV 10.10.237.176", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-15 00:14 CET
Warning: 10.10.237.176 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.237.176
Host is up (0.080s latency).
Not shown: 65531 closed tcp ports (reset)
PORT    STATE SERVICE     VERSION
22/tcp  open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 10:8a:f5:72:d7:f9:7e:14:a5:c5:4f:9e:97:8b:3d:58 (RSA)
|   256 7f:10:f5:57:41:3c:71:db:b5:5b:db:75:c9:76:30:5c (ECDSA)
|_  256 6b:4c:23:50:6f:36:00:7c:a6:7c:11:73:c1:a8:60:0c (ED25519)
80/tcp  open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-title: Apache2 Ubuntu Default Page: It works
|_http-server-header: Apache/2.4.18 (Ubuntu)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
Service Info: Host: TECHSUPPORT; OS: Linux; CPE: cpe:/o:linux:linux_kernel")}}

{{text("We find 4 open ports: ")}}

{{list(['22 (SSH)', '80 (HTTP)', '139 (SMB)', '445 (SMB)'])}}

{{header("SMB", "smb")}}

{{text("We begin with checking if there is anything to find in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SMB</code> service.")}}

{{text("We can use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>enum4linux</code> to check for existing shares.")}}

{{console("enum4linux 10.10.237.176", "...
=================================( Share Enumeration on 10.10.237.176 )=================================
                                                                                                                     
                                                                                                                     
        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        websvr          Disk      
        IPC$            IPC       IPC Service (TechSupport server (Samba, Ubuntu))
Reconnecting with SMB1 for workgroup listing.

        Server               Comment
        ---------            -------

        Workgroup            Master
        ---------            -------
        WORKGROUP   
...")}}

{{text("We find 3 shares, out of which <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>websvr</code> looks the most promising. Let's connect to it.")}}

{{text("There is a text file on that share. We can download it onto our machine.")}}

{{image("../../static/writeups/techsupport/images/000001.jpg")}}

{{console("cat enter.txt", "GOALS
=====
1)Make fake popup and host it online on Digital Ocean server
2)Fix subrion site, /subrion doesn't work, edit from panel
3)Edit wordpress website

IMP
===
Subrion creds
|->admin:[REDACTED] [cooked with magical formula]
Wordpress creds
|->
")}}

{{text("We find some admin credentials and find out about a possible <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/subrion</code> directory on the web page.")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{text("Just like in the text, <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/subrion</code> directory doesn't seem to work. That doesn't stop us from further enumerating this directory.")}}

{{console("ffuf -u http://10.10.237.176/subrion/FUZZ -w  /usr/share/wordlists/dirb/big.txt -fl 1 -fw 20", "
        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://10.10.237.176/subrion/FUZZ
 :: Wordlist         : FUZZ: /usr/share/wordlists/dirb/big.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-299,301,302,307,401,403,405,500
 :: Filter           : Response words: 20
 :: Filter           : Response lines: 1
________________________________________________

favicon.ico             [Status: 200, Size: 1150, Words: 10, Lines: 4, Duration: 81ms]
robots.txt              [Status: 200, Size: 142, Words: 9, Lines: 8, Duration: 75ms]
sitemap.xml             [Status: 200, Size: 628, Words: 6, Lines: 4, Duration: 69ms]
:: Progress: [20469/20469] :: Job [1/1] :: 448 req/sec :: Duration: [0:00:45] :: Errors: 0 ::")}}

{{text("We find a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>robots.txt</code> file. In it are a couple of entries but what interests us the most is the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/subrion/panel</code> directory.")}}

{{image("../../static/writeups/techsupport/images/000002.jpg")}}

{{text("This is where we most likely will use the password we found, but we have to decode it first.")}}

{{text("We input the string we find into <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>CyberChef</code> and click on the magic wand. It will automatically decode the password for us.")}}

{{image("../../static/writeups/techsupport/images/000003.jpg")}}

{{text("Now we simply log in.")}}

{{image("../../static/writeups/techsupport/images/000004.jpg")}}

{{text("It says <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Subrion CMS v4.2.1</code>. We can go and try to find an exploit for that version.")}}

{{link("https://www.exploit-db.com/exploits/49876", "https://www.exploit-db.com/favicon.ico", "Subrion CMS 4.2.1 - Arbitrary File Upload")}}

{{text("We copy the exploit and run it with the correct parameters.")}}

{{image("../../static/writeups/techsupport/images/000004.jpg")}}

{{header}}

{{text("While looking through the file system, I was able to find MySQL credentials in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/var/html/www/wordpress/wp-config.php</code> file.")}}

{{text("I also found out that a user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>scamsite</code> existed on the machine.")}}

{{text("I was curious if he reused his passwords and tried logging via SSH as him, and it worked.")}}

{{image("../../static/writeups/techsupport/images/000005.jpg")}}

{{header("Flag", "flag")}}

{{text("Since we knew our current user password, I checked his sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for scamsite on TechSupport:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User scamsite may run the following commands on TechSupport:
    (ALL) NOPASSWD: /usr/bin/iconv")}}

{{text("A quick search on <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>GTFOBins</code> and we know how to exploit it.")}}

{{image("../../static/writeups/techsupport/images/000006.jpg")}}

{{text("Knowing that we can read any file, we can simply read the flag.")}}

{{image("../../static/writeups/techsupport/images/000007.jpg")}}

{{script()}}









