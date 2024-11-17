{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("Let us start by scanning all the ports.")}}

{{console("nmap -T5 -p- 10.10.209.122", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-15 09:23 CET
Nmap scan report for 10.10.209.122
Host is up (0.090s latency).
PORT     STATE SERVICE
22/tcp   open  ssh
8000/tcp open  http-alt
")}}

{{text("After visiting the site on port 8000, we are returned this.")}}

{{image("../../static/images/pyrat/000001.jpg")}}

{{text("I tried using Burp, but that didn't lead to anywhere. After that I used netcat to try and connect to this address. Since it is stated that <code class='bg-gray-300 rounded-md px-1'>a HTTP response leads to Python code vulnerability</code> I instantly tried to run python code.")}}

{{console("nc 10.10.209.122 8000", "l
name 'l' is not defined
test
name 'test' is not defined
print(2)
2
")}}

{{text("Since it worked, I got a python reverse shell from <code class='bg-gray-300 rounded-md px-1'>revshells.com</code> and tried to get it to run.")}}

{{image("../../static/images/pyrat/000002.jpg")}}

{{text("That worked and now we were the <code class='bg-gray-300 rounded-md px-1'>www-data</code> user.")}}

{{text("While looking through the system, I noticed a <code class='bg-gray-300 rounded-md px-1'>.git</code> directory inside of <code class='bg-gray-300 rounded-md px-1'>/opt/dev</code>.")}}

{{text("Challange description said that we have to <code class='bg-gray-300 rounded-md px-1'>explore into application's older version</code> so I tried to do that.")}}

{{text("Reading through the files inside <code class='bg-gray-300 rounded-md px-1'>.git</code> directory, we stumble across an old <code class='bg-gray-300 rounded-md px-1'>config</code> file that contains user credentials.")}}

{{console("cat config", "[core]
        repositoryformatversion = 0
        filemode = true
        bare = false
        logallrefupdates = true
[user]
        name = Jose Mario
        email = josemlwdf@github.com

[credential]
        helper = cache --timeout=3600

[credential 'https://github.com']
        username = think
        password = [REDACTED]")}}

{{text("We switch users to <code class='bg-gray-300 rounded-md px-1'>think</code> and using the newly acquired password we successfully log in.")}}

