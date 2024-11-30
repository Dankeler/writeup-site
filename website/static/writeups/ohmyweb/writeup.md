{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start by scanning the ports.")}}

{{console("nmap -T5 -p- -sV -sC 10.10.19.156", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-29 14:47 CET
Nmap scan report for 10.10.19.156
Host is up (0.13s latency).
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 e0:d1:88:76:2a:93:79:d3:91:04:6d:25:16:0e:56:d4 (RSA)
|   256 91:18:5c:2c:5e:f8:99:3c:9a:1f:04:24:30:0e:aa:9b (ECDSA)
|_  256 d1:63:2a:36:dd:94:cf:3c:57:3e:8a:e8:85:00:ca:f6 (ED25519)
80/tcp open  http    Apache httpd 2.4.49 ((Unix))
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.49 (Unix)
|_http-title: Consult - Business Consultancy Agency Template | Home
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
")}}

{{text("We discover 2 open ports: ")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("We should notice that the web server on port 80 is running on <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Apache/2.4.49</code>.")}}

{{header("Shell as daemon", "shell-as-daemon")}}

{{text("We don't even have to visit the web page, because after searching for exploits for that version, we get ton of results. We find out it's the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>CVE-2021-41773</code> vulnerability.")}}

{{link("https://blog.qualys.com/vulnerabilities-threat-research/2021/10/27/apache-http-server-path-traversal-remote-code-execution-cve-2021-41773-cve-2021-42013", "https://ik.imagekit.io/qualys/wp-content/uploads/2017/07/cropped-qualys-150x150.png", "Apache HTTP Server Path Traversal & Remote Code Execution (CVE-2021-41773 & CVE-2021-42013)")}}

{{text("We should test if it works by sending one of the provided requests.")}}

{{image("../../static/writeups/ohmyweb/images/000001.jpg")}}

{{text("This folder exists, but we don't have neccessary permissions which is fine. Let's try to get a RCE now.")}}

{{text("We set up a netcat listener and send a reverse shell from <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code>.")}}

{{image("../../static/writeups/ohmyweb/images/000002.jpg")}}

{{text("It works and now we can upgrade our shell.")}}

{{image("../../static/writeups/ohmyweb/images/000003.jpg")}}

{{header("Root on docker", "root-on-docker")}}

{{text("I found out we are in a docker container by the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.dockerenv</code> file in the root directory but I couldn't find anything else.")}}

{{text("After a while I listed the enabled capabilities and found this.")}}

{{console("getcap -r / 2>/dev/null", "/usr/bin/python3.7 = cap_setuid+ep")}}

{{text("A quick search on <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>GTFOBins</code> and we find this.")}}

{{link("https://gtfobins.github.io/gtfobins/python/#capabilities", "https://gtfobins.github.io/assets/logo.png", "python | Capabilities | GTFOBins")}}

{{text("We use the provided command and get root access (on the docker container).")}}

{{header("Root flag", "root-flag")}}

{{text("Now we need to break out the docker container.")}}

{{text("After further enumeration and running <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ifconfig</code> I found another machine running.")}}

{{image("../../static/writeups/ohmyweb/images/000004.jpg")}}

{{text("I downloaded a nmap binary from <a>here</a> onto my machine and hosted a http server with <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>python3 -m http.server</code>. Since there is no <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>wget</code> on the docker container I had to use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>curl</code>.")}}

{{image("../../static/writeups/ohmyweb/images/000005.jpg")}}

{{text("I made the binary executable and checked for any open ports that we didn't know of.")}}

{{text("We find ports <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>5985</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>5986</code>.")}}

{{text("While searching for exploits for port 5986, I came across this page.")}}

{{link("https://github.com/AlteredSecurity/CVE-2021-38647/blob/main/CVE-2021-38647.py", "../../static/writeups/images/github.jpg", "CVE-2021-38647.py")}}

{{text("We download this python file onto our machine, then we use curl like before to get it onto the victim's machine.")}}

{{text("We make the exploit executable and run it in order to read the flag.")}}

{{console("python3 exploit.py -t 172.17.0.1  -c 'cat /root/root.txt'", "[REDACTED]")}}

{{script()}}