{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start off by scanning all the ports.")}}

{{console("nmap -T5 -p- -sC 10.10.95.2", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-10 01:32 CET
Warning: 10.10.95.2 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.95.2
Host is up (0.071s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
| ssh-hostkey: 
|   3072 82:be:d6:b4:5d:13:27:98:e1:c1:a3:fd:3c:7c:db:83 (RSA)
|   256 bf:9c:75:78:9a:05:5a:9e:94:9d:c3:f6:59:e0:3c:9c (ECDSA)
|_  256 4e:2b:c6:ed:cf:c3:2f:e6:e7:43:f5:cb:62:17:8a:93 (ED25519)
80/tcp open  http
|_http-title: Lo-Fi Music

Nmap done: 1 IP address (1 host up) scanned in 204.92 seconds")}}

{{text("We find 2 open ports:")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("Let's begin by checking out the web page.")}}

{{image("../../static/writeups/lofi/images/000001.jpg")}}

{{text("Upon clicking on the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Discography</code> links a parameter gets added to the URL and the displayed video changes.")}}

{{image("../../static/writeups/lofi/images/000002.jpg")}}

{{text("Since <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sleep.php</code> is probably a file, I wondered if <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>LFI</code> (Local File Inclusion) is possible.")}}

{{text("A couple of tries and I was successful in reading the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/passwd</code> file.")}}

{{text("Since the room's tells us the flag is <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>in the root of the filesystem</code>, I tried reading it.")}}

{{image("../../static/writeups/lofi/images/000003.jpg")}}

{{script()}}