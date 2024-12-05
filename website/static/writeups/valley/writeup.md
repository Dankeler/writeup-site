{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We run a basic port scan.")}}

{{console("nmap -T5 -p- 10.10.158.231", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-03 17:21 CET
Warning: 10.10.158.231 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.158.231
Host is up (0.082s latency).
Not shown: 56437 closed tcp ports (conn-refused), 9095 filtered tcp ports (no-response)
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
37370/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 468.07 seconds")}}


{{text("We get back a page for a photographic company. We are able to view their gallery of photos and pricing options.")}}

{{image("../../static/writeups/valley/images/000001.jpg")}}

{{text("I noticed an interesting detail in the URL structure when clicking on a photo from the gallery.")}}

{{image("../../static/writeups/valley/images/000002.jpg")}}

{{text("Maybe if we change <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>1</code> to something different we might find something hidden?")}}

{{text("I created a wordlist with numbers from 0 to 10000 and used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ffuf</code> to go over those endpoints but I didn't end up finding anything.")}}

{{text("Then I just started entering in numbers manually while hoping that one of them is correct and I was right.")}}

{{text("<code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>00</code> is the correct number.")}}

{{image("../../static/writeups/valley/images/000003.jpg")}}

{{text("In the notes we see another endpoint, <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/dev1243224123123</code>. Let's see if it's still up.")}}

{{image("../../static/writeups/valley/images/000004.jpg")}}

{{text("It is a log in page for the developers of the website. We should look around and try to find something hidden.")}}

{{text("While looking through the source code of the website I found a script tag with source of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>dev.js</code>. After looking through it I was able to find valid credentials.")}}

{{image("../../static/writeups/valley/images/000005.jpg")}}

{{text("We now can log in using the credentials or simply go to the provided endpoint.")}}

{{image("../../static/writeups/valley/images/000006.jpg")}}

{{header("FTP Server", "ftp-server")}}

{{text("The note is about the FTP server and changing its port to the default one. We can guess that the service running at port <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>37370</code> is the FTP server without having to scan it further.")}}

{{text("It also mentions not reusing credentials so my guess is that the credentials from before will work on the FTP server.")}}

{{text("We try to login using the same credentials and it works.")}}

{{image("../../static/writeups/valley/images/000007.jpg")}}

{{text("By listing all the files we find 3 <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>pcapng</code> files. We should download them.")}}

{{text("We use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>mget *</code> to download multiple files at once.")}}

{{image("../../static/writeups/valley/images/000008.jpg")}}

{{text("Now we can use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Wireshark</code> to analyze those files.")}}

{{text("I found an interesting POST request in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>siemHTTP2.pcapng</code> file.")}}

{{image("../../static/writeups/valley/images/000009.jpg")}}

{{text("I clicked on the request to analyze it further and found a username and password.")}}

{{image("../../static/writeups/valley/images/000010.jpg")}}

{{text("Since we were logged in the website and FTP server already my guess was this were the credentials to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SSH</code>.")}}

{{image("../../static/writeups/valley/images/000011.jpg")}}

{{header("Shell as root", "shell-as-root")}}

{{text("It worked and now we are logged in as the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>valleyDev</code> user.")}}

{{text("In the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/home</code> directory we are able to find a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>valleyAuthenticator</code> file.")}}

{{text("We can download it by setting up a python http server and using wget to download it.")}}

{{text("Then I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ghidra</code> to reverse engineer the file. I searched for strings and found a hashed password which was <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>e6722920bab23[REDACTED]</code>.")}}

{{text("By going to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>hashes.com</code> and checking our strings that look like hashes we are able to find the password.")}}

{{image("../../static/writeups/valley/images/000012.jpg")}}

{{text("By checking for other users in <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/passwd</code> file we find a user named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>valley</code>. We use our password to login as that user.")}}

{{image("../../static/writeups/valley/images/000013.jpg")}}

{{text("I ran <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>linpeas</code> and found a cronjob that will run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/photos/script/photosEncrypt.py</code> every minute.")}}

{{console("cat photosEncrypt.py", "#!/usr/bin/python3
import base64
for i in range(1,7):
# specify the path to the image file you want to encode
	image_path = '/photos/p' + str(i) + '.jpg'

# open the image file and read its contents
	with open(image_path, 'rb') as image_file:
          image_data = image_file.read()

# encode the image data in Base64 format
	encoded_image_data = base64.b64encode(image_data)

# specify the path to the output file
	output_path = '/photos/photoVault/p' + str(i) + '.enc'

# write the Base64-encoded image data to the output file
	with open(output_path, 'wb') as output_file:
    	  output_file.write(encoded_image_data)")}}

{{text("Nothing in this script looks exploitable, but I found out that we have write permissions to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/usr/lib/python3.8/base64.py</code> which is the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>import base64</code> line.")}}

{{text("If we run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>echo 'import os;os.system('chmod u+s /bin/bash')' > /usr/lib/python3.8/base64.py</code> it should allow us to run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/bin/bash</code> as the root.")}}

{{text("This will set the SUID bit on <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/bin/bash</code>, allowing us to execute it with root privileges by running <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/bin/bash -p</code>.")}}

{{image("../../static/writeups/valley/images/000014.jpg")}}

{{script()}}
