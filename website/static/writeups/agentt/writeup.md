{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We begin by scanning all the ports.")}}

{{console("nmap -T5 -p- 10.10.109.161", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-14 01:43 CET
Nmap scan report for 10.10.109.161
Host is up (0.076s latency).
Not shown: 65420 closed tcp ports (reset), 114 filtered tcp ports (no-response)
PORT   STATE SERVICE
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 229.96 seconds")}}

{{text("I think this is my first time seeing no SSH service running.")}}

{{text("Anyways, let's proceed with checking out the web page.")}}

{{image("../../static/writeups/agentt/images/000001.jpg")}}

{{text("It is a admin dashboard for some kind of business.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Website was pretty much all static with nothing interesting on it. Directory scan also didn't reveal anything of interest.")}}

{{text("I checked a extension named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Wappalyzer</code> which is used to check what technologies are being used on a site and it said the version of PHP being used was <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>8.1.0</code>.")}}

{{text("A quick search returns a lot of exploits for that version.")}}

{{link("https://www.exploit-db.com/exploits/49933", "https://www.exploit-db.com/favicon.ico", "PHP 8.1.0-dev - 'User-Agentt' Remote Code Execution")}}

{{text("I downloaded the exploit and used it against the website.")}}

{{image("../../static/writeups/agentt/images/000002.jpg")}}

{{text("We can find the flag in the root directory.")}}

{{image("../../static/writeups/agentt/images/000003.jpg")}}

{{script()}}