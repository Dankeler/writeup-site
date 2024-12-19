{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("I started by running a port scan.")}}

{{console("nmap -T5 -p- 10.10.56.250", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-07 16:32 CET
Warning: 10.10.56.250 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.56.250
Host is up (0.068s latency).
Not shown: 57153 closed tcp ports (conn-refused), 8376 filtered tcp ports (no-response)
PORT     STATE SERVICE
22/tcp   open  ssh
80/tcp   open  http
222/tcp  open  rsh-spx
1337/tcp open  waste
3000/tcp open  ppp
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 462.23 seconds")}}

{{text("We find a lot of open ports. The one I would focus on is the port <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>80</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>8080</code>.")}}