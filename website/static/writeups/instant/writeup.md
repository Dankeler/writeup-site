{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start off by scanning all the ports.")}}

{{console("nmap -T5 -p- -sC -sV 10.10.11.37", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-27 22:00 CET
Warning: 10.10.11.37 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.11.37
Host is up (0.053s latency).
Not shown: 64876 closed tcp ports (reset), 657 filtered tcp ports (no-response)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.5 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 31:83:eb:9f:15:f8:40:a5:04:9c:cb:3f:f6:ec:49:76 (ECDSA)
|_  256 6f:66:03:47:0e:8a:e0:03:97:67:5b:41:cf:e2:c7:c7 (ED25519)
80/tcp open  http    Apache httpd 2.4.58
|_http-server-header: Apache/2.4.58 (Ubuntu)
|_http-title: Did not follow redirect to http://instant.htb/
Service Info: Host: instant.htb; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 433.81 seconds")}}

{{text("We find 2 open ports:")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("Let's proceed with checking out the web page.")}}

{{text("Before we can do that, we of course have to add an entry to our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file.")}}

{{console("echo '10.10.11.37 instant.htb' >> /etc/hosts")}}

{{image("../../static/writeups/instant/images/000001.jpg")}}

{{text("It is a page for downloading a mobile app used to transfer funds between accounts.")}}

{{header("APK file", "apk-file")}}

{{text("Since I couldn't find anything interesting, I downloaded the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.apk</code> file in hopes that it contained something valuable.")}}

{{text("I used a tool called <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>apktool</code> on the downloaded file.")}}

{{console("apktool d instant.apk")}}

{{text("Looking through the files, I found an interesting file at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/smali/com/instantlabs/instant/AdminActivities.smali</code>.")}}

{{console("cat AdminActivities.smali", "...
invoke-direct {v1}, Lokhttp3/Request$Builder;-><init>()V

    const-string v2, 'http://mywalletv1.instant.htb/api/v1/view/profile

    .line 24
    invoke-virtual {v1, v2}, Lokhttp3/Request$Builder;->url(Ljava/lang/String;)Lokhttp3/Request$Builder;

    move-result-object v1

    const-string v2, 'Authorization'

    const-string v3, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwicm9sZSI6IkFkbWluIiwid2FsSWQiOiJmMGVjYTZlNS03ODNhLTQ3MWQtOWQ4Zi0wMTYyY2JjOTAwZGIiLCJleHAiOjMzMjU5MzAzNjU2fQ.v0qyyAqDSgyoNFHU7MgRQcDA0Bw99_8AEXKGtWZ6rYA'
...")}}

{{text("It contained what looked like a hardcoded <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>JWT</code> authorization token together with an endpoint.")}}

{{text("I queried this endpoint while providing the found JWT token.")}}

{{image("../../static/writeups/instant/images/000002.jpg")}}

{{text("In the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/res/xml/network_security_config.xml</code> file there was yet another endpoint.")}}

{{console("cat network_security_config.xml", "<?xml version='1.0' encoding='utf-8'?>
<network-security-config>
    <domain-config cleartextTrafficPermitted='true'>
        <domain includeSubdomains='true'>mywalletv1.instant.htb</domain>
        <domain includeSubdomains='true'>swagger-ui.instant.htb</domain>
    </domain-config>
</network-security-config>")}}

{{text("After adding that subdomain to my <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file, I visited it.")}}

{{header("Shell as shirohige", "shell-as-shirohige")}}

{{image("../../static/writeups/instant/images/000003.jpg")}}

{{text("There were even more endpoints to visit.")}}

{{text("The <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/api/v1/admin/view/logs</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/api/v1/admin/read/log</code> looked the most useful.")}}

{{image("../../static/writeups/instant/images/000004.jpg")}}

{{text("By providing the JWT token, I was able to query this endpoint. It seemed like it gave me a directory listing of the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/home/shirohige/logs/</code> directory.")}}

{{text("Then I used the other endpoint to read the contents of that file.")}}

{{image("../../static/writeups/instant/images/000005.jpg")}}

{{text("I immedietialy though of a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Local File Inclusion</code> (LFI) attack.")}}

{{text("To confirm my suspicions I tried reading the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/passwd</code> file.")}}

{{image("../../static/writeups/instant/images/000006.jpg")}}

{{text("I was right. What we can do now is try to find some sort of credentials.")}}

{{image("../../static/writeups/instant/images/000007.jpg")}}

{{text("Now we had the private key of the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>shirohige</code> user.")}}

{{text("We paste it into a file and log in.")}}

{{image("../../static/writeups/instant/images/000008.jpg")}}

{{header("Shell as root", "shell-as-root")}}

{{text("In the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>~/projects/mywallet/Instant-Api/mywallet/instance</code> directory I found a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>instant.db</code> database file.")}}

{{text("I downloaded the file onto my machine.")}}

{{image("../../static/writeups/instant/images/000009.jpg")}}

{{text("I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sqlitebrowser</code> to read the database.")}}

{{image("../../static/writeups/instant/images/000010.jpg")}}

{{text("It contained a table with users and their hashed passwords.")}}

{{text("I found this tool that will help us with cracking those passwords.")}}

{{link("https://github.com/Mrterrestrial/WerkzeugHashCracker", "../../static/writeups/images/github.jpg", "Dictionary Attack Tool for Werkzeug Password Hashes")}}

{{text("For some reason I was unable to crack these passwords?? Thankfully it doesn't matter because I found a different way to exploit this machine.")}}

{{text("In the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt/backups/Solar-PuTTY</code> directory is a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sessions-backup.dat</code> file.")}}

{{text("By downloading this file onto my machine and by using a tool named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SolarPuttyCracker</code> I was able to crack the password to it.")}}

{{link("https://github.com/ItsWatchMakerr/SolarPuttyCracker/tree/main", "../../static/writeups/images/github.jpg", "SolarPuttyCracker")}}

{{console("python3 SolarPuttyCracker.py sessions-backup.dat -w /usr/share/wordlists/rockyou.txt", "
   ____       __             ___         __   __          _____                 __            
  / __/___   / /___ _ ____  / _ \ __ __ / /_ / /_ __ __  / ___/____ ___ _ ____ / /__ ___  ____
 _\ \ / _ \ / // _ `// __/ / ___// // // __// __// // / / /__ / __// _ `// __//  '_// -_)/ __/
/___/ \___//_/ \_,_//_/   /_/    \_,_/ \__/ \__/ \_, /  \___//_/   \_,_/ \__//_/\_\ \__//_/   
                                                /___/                                         
Trying to decrypt using passwords from wordlist...
Decryption successful using password: [REDACTED]
[+] DONE Decrypted file is saved in: SolarPutty_sessions_decrypted.txt")}}

{{text("In the outputted file was the root's password.")}}

{{image("../../static/writeups/instant/images/000011.jpg")}}

{{script()}}