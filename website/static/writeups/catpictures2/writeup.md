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

{{header("Cat Gallery",  "cat-gallery")}}

{{text("We visit the web page on port 80.")}}

{{image("../../static/writeups/catpictures2/images/000001.jpg")}}

{{text("It is a gallery with cat pictures.")}}

{{text("When I chose the first picture and clicked onto <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>About photo</code> in the top right, I saw a note.")}}

{{image("../../static/writeups/catpictures2/images/000002.jpg")}}

{{text("I downloaded the picture for further analysis.")}}

{{text("I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>exiftool</code> on the file.")}}

{{image("../../static/writeups/catpictures2/images/000003.jpg")}}

{{text("It seems there is a hidden text file on the web page on port 8080.")}}

{{image("../../static/writeups/catpictures2/images/000004.jpg")}}

{{text("We get credentials to a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>gitea</code> instance that is running on port <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>3000</code>")}}

{{header("Ansible Playbook", "ansible-playbook")}}

{{text("We proceed to the web page and log in with the given credentials.")}}

{{text("We notice a repository named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ansible</code> that contains a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.yaml</code> file.")}}

{{text("If we navigate to the page on port <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>1337</code> we get a page from which we can execute our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.yaml</code> file by clicking on the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Run Ansible Playbook</code> option.")}}

{{text("If we change the command from <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>whoami</code> to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ls</code> and look at  the logs, we see that our command gets executed and we even found the second flag. We could read it from here using the same method.")}}

{{image("../../static/writeups/catpictures2/images/000005.jpg")}}

{{text("We should try to check for user's credentials that would allow us to log in via SSH.")}}

{{text("We could try to get the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id_rsa</code> of our current user by changing the command once more.")}}

{{text("We read the private key from our user's home directory.")}}

{{image("../../static/writeups/catpictures2/images/000006.jpg")}}

{{text("Now we can log in via SSH by providing this private key.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("I ran <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>linpeas</code> on the target machine and noticed that the sudo version is <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>1.8.21p2</code>.")}}

{{text("After a quick search for an exploit to that version I found one.")}}

{{link("https://github.com/blasty/CVE-2021-3156", "../../static/writeups/images/github.jpg", "CVE-2021-3156 PoC")}}

{{text("We use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>git clone</code> in order to download it onto our machine. We can use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>tar</code> to compress the folder.")}}

{{text("Then we set up a python web server and download it using wget.")}}

{{text("Then we run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>make</code> to build the exploit and run it.")}}

{{image("../../static/writeups/catpictures2/images/000007.jpg")}}

{{script()}}