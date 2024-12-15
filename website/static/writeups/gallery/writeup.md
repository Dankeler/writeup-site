{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start off by scanning all the ports.")}}

{{console("nmap -T5 -p- 10.10.36.37", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-14 10:10 CET
Warning: 10.10.47.146 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.47.146
Host is up (0.076s latency).
Not shown: 65533 closed tcp ports (reset)
PORT     STATE SERVICE
80/tcp   open  http
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 318.88 seconds")}}

{{text("We discover only 2 open ports: ")}}

{{list(['80 (HTTP)', '8080 (HTTP)'])}}

{{text("I visited the page at port 80, but it contained only a default Apache page, so I proceeded with port 8080.")}}

{{image("../../static/writeups/gallery/images/000001.jpg")}}

{{text("So the CMS being used is Simple Image Gallery. Let's search for any known exploits.")}}

{{link("https://www.exploit-db.com/exploits/50214", "https://www.exploit-db.com/favicon.ico", "Simple Image Gallery 1.0 - Remote Code Execution (RCE) (Unauthenticated)")}}

{{text("We don't even have to run the exploit because if we take a look at the line <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>post_data = {'username': 'admin' or '1'='1'#', 'password': ""}</code> we see the payload used for authentication bypassing.")}}

{{text("If we simply use it in the username field, we should be able to log in.")}}

{{image("../../static/writeups/gallery/images/000002.jpg")}}

{{text("We have access to the admin panel now. Now we can simply upload a PHP file with a reverse shell as one of the images, set up a listener and execute it.")}}

{{image("../../static/writeups/gallery/images/000003.jpg")}}

{{header("Shell as mike", "shell-as-mike")}}

{{text("While looking through the files, I found an interesting <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/backups</code> inside of the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/var</code> directory.")}}

{{text("There was another directory for the user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>mike</code>. Inside of it was a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.bash_history</code> file that contained his password.")}}

{{console("cat .bash_history", "cd ~
ls
ping 1.1.1.1
cat /home/mike/user.txt
cd /var/www/
ls
cd html
ls -al
cat index.html
sudo -l [REDACTED]
clear
sudo -l
exit")}}

{{text("Using that we can now switch users.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Since we knew our user password, I checked his sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for mike on gallery:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User mike may run the following commands on gallery:
    (root) NOPASSWD: /bin/bash /opt/rootkit.sh")}}

{{text("We check the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>rootkit.sh</code> file.")}}

{{console("cat rootkit.sh", "#!/bin/bash

read -e -p 'Would you like to versioncheck, update, list or read the report ? ' ans;

# Execute your choice
case $ans in
    versioncheck)
        /usr/bin/rkhunter --versioncheck ;;
    update)
        /usr/bin/rkhunter --update;;
    list)
        /usr/bin/rkhunter --list;;
    read)
        /bin/nano /root/report.txt;;
    *)
        exit;;
esac")}}

{{text("Since we will run this file as sudo, the binaries used will get sudo privilages as well. Following that, we can check <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>GTFOBins</code> for a way to privilage escalate using these.")}}

{{text("We find that we can use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>nano</code> to gain elevated privilages.")}}

{{link("https://gtfobins.github.io/gtfobins/nano/", "https://gtfobins.github.io/assets/logo.png", "nano | GTFOBins")}}

{{text("We simply run the script with sudo and choose the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>read</code> option. When the report opens, we follow the commands provided and  we should get a shell as root.")}}

{{script()}}