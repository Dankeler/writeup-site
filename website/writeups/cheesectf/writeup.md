{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Enumeration", "enumeration")}}

{{text("Running Nmap scan yields a lot, and I mean a lot of open ports. Almost all of them are not meaningful, and are there to throw us off.")}}

{{text("Ports that we should focus on are:")}}

{{list(['22 (SSH)', '80 (HTTP)'])}}

{{text("Upon visting port 80 we are presented a cheese shop page.")}}

{{image("../../static/images/cheesectf/000001.jpg")}}

{{text("There is also a login page.")}}

{{image("../../static/images/cheesectf/000002.jpg")}}

{{text("We should test if <code class='bg-gray-300 rounded-md px-1'>SQL Injection</code> will work on this form.")}}

{{text("We catch the request using Burp suite and then try to use it in SQLMap")}}

{{image("../../static/images/cheesectf/000003.jpg")}}

{{console("sqlmap -r request.txt", "...
got a 302 redirect to 'http://10.10.229.61/secret-script.php?file=supersecretadminpanel.html'. Do you want to follow? [Y/n] 
...")}}

{{text("We can see that SQLMap got redirected to <code class='bg-gray-300 rounded-md px-1'>?file=supersecretadminpanel.html</code>. We can try to go to this URL.")}}

{{image("../../static/images/cheesectf/000004.jpg")}}

{{text("We access the admin panel for the website.")}}

{{text("There is an interesting <code class='bg-gray-300 rounded-md px-1'>?file</code> parameter together with a <code class='bg-gray-300 rounded-md px-1'>php://filter</code>.")}}




