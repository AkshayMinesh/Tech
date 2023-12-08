from flask import Flask, render_template, request
import time
from base64 import standard_b64encode, standard_b64decode

app = Flask(__name__, template_folder='templates')

def b64_to_str(b64: str) -> str:
    bytes_b64 = b64.encode('ascii')
    bytes_str = standard_b64decode(bytes_b64)
    __str = bytes_str.decode('ascii')
    return __str
def str_to_b64(__str: str) -> str:
    str_bytes = __str.encode('ascii')
    bytes_b64 = standard_b64encode(str_bytes)
    b64 = bytes_b64.decode('ascii')
    return b64
idk = "NjAyOA=="
cc = int(b64_to_str(idk))
correct_codes = [f"{cc}"]


    
login_attempts = 0
last_attempt_time = 0

def check_code(code):
    return code in correct_codes

def impose_timeout():
    global last_attempt_time
    last_attempt_time = time.time()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check_code', methods=['POST'])
def check_code_route():
    global login_attempts

    if time.time() - last_attempt_time < 30:
        time_remaining = int(30 - (time.time() - last_attempt_time))
        return f"Too many attempts. Please wait for {time_remaining} seconds before trying again."

    entered_code = request.form.get('code')

    # Check if the code is correct
    if check_code(entered_code):
        # Reset login attempts on successful login
        login_attempts = 0
        return render_template('win.html')  # Render the win template

    else:
        login_attempts += 1

        if login_attempts == 4:
            impose_timeout()
            login_attempts = 0
            return f"Too many incorrect attempts. Please wait for 30 seconds before trying again." + """
            <script>
                var countdown = 30;
                var countdownInterval = setInterval(function() {
                    countdown -= 1;
                    document.getElementById('countdown').innerHTML = countdown;
                    if (countdown <= 0) {
                        clearInterval(countdownInterval);
                        window.location.href = '/';
                    }
                }, 1000);
            </script>
            <p>Redirecting in <span id='countdown'>30</span> seconds...</p>
            """
        time_remaining = int(10 - (time.time() - last_attempt_time))
        return f"Incorrect code.\nNote: A 30 seconds timeout will be imposed on 3 wrong attempts in a row." + """
            <script>
                var countdown = 10;
                var countdownInterval = setInterval(function() {
                    countdown -= 1;
                    document.getElementById('countdown').innerHTML = countdown;
                    if (countdown <= 0) {
                        clearInterval(countdownInterval);
                        window.location.href = '/';
                    }
                }, 1000);
            </script>
            <p>Redirecting in <span id='countdown'>10</span> seconds...</p>
            """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)


