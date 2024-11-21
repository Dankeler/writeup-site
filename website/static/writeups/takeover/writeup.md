{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We run a basic port scan.")}}

{{console("nmap -T5 -p- 10.10.239.226", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-19 23:51 CET
Nmap scan report for 10.10.239.226
Host is up (0.080s latency).
PORT    STATE SERVICE
22/tcp  open  ssh
80/tcp  open  http
443/tcp open  https

Nmap done: 1 IP address (1 host up) scanned in 37.77 seconds")}}

{{text("We find 3 open ports: ")}}

{{list(['22 (SSH)', '80 (HTTP)', '443 (HTTPS)'])}}

{{text("We begin by enumerating the subdomains using <code class='bg-gray-300 rounded-md px-1'>ffuf</code>.")}}

{{console("ffuf -w /usr/share/wordlists/dirb/common.txt -H 'Host: FUZZ.futurevera.thm' -u https://10.10.239.226 -fs 4605", "...
blog                    [Status: 200, Size: 3838, Words: 1326, Lines: 81, Duration: 100ms]
Blog                    [Status: 200, Size: 3838, Words: 1326, Lines: 81, Duration: 95ms]
Support                 [Status: 200, Size: 1522, Words: 367, Lines: 34, Duration: 93ms]
support                 [Status: 200, Size: 1522, Words: 367, Lines: 34, Duration: 93ms]
:: Progress: [4614/4614] :: Job [1/1] :: 497 req/sec :: Duration: [0:00:11] :: Errors: 0 ::")}}

{{text("We find <code class='bg-gray-300 rounded-md px-1'>support</code> and <code class='bg-gray-300 rounded-md px-1'>blog</code> subdomains.")}}

{{text("Let's add <code class='bg-gray-300 rounded-md px-1'>https://futurevera.thm</code> as well as <code class='bg-gray-300 rounded-md px-1'>https://support.futurevera.thm</code> and <code class='bg-gray-300 rounded-md px-1'>https://blog.futurevera.thm</code> to our <code class='bg-gray-300 rounded-md px-1'>/etc/hosts</code> file.")}}

{{console("127.0.0.1       localhost
127.0.1.1       DESKTOP-33R7692.        DESKTOP-33R7692
10.10.239.226   blog.futurevera.thm support.futurevera.thm futurevera.thm

# The following lines are desirable for IPv6 capable hosts
::1     ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters")}}

{{text("While looking for attack vectors, I noticed something in the <code class='bg-gray-300 rounded-md px-1'>https://support.futurevera.thm</code> certificate.")}}

{{image("../../static/writeups/takeover/images/000001.jpg")}}

{{text("There was a hidden subdomain in the <code class='bg-gray-300 rounded-md px-1'>DNS Name</code> field.")}}

{{image("../../static/writeups/takeover/images/000002.jpg")}}

{{text("After adding that subdomain to our <code class='bg-gray-300 rounded-md px-1'>/etc/hosts</code> file and visiting it, we get the flag.")}}

{{image("../../static/writeups/takeover/images/000003.jpg")}}

{{script()}}