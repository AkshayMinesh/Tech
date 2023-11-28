import http.server
import socketserver
import time
import os

# Correct codes
correct_codes = ["asdfe564", "safasfe654", "hre534tged"]

# Variables to track login attempts
login_attempts = 0
last_attempt_time = 0

# Function to check if the code is correct
def check_code(code):
    return code in correct_codes

# Function to impose a timeout after 3 failed attempts
def impose_timeout():
    global last_attempt_time
    last_attempt_time = time.time()

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Serve the homepage
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            # Serve static files
            super().do_GET()

    def do_POST(self):
        global login_attempts

        # Check if a timeout is in effect
        if time.time() - last_attempt_time < 30:
            time_remaining = int(30 - (time.time() - last_attempt_time))
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"Too many attempts. Please wait for {time_remaining} seconds before trying again.".encode())
            return

        # Get the entered code from the form
        content_length = int(self.headers['Content-Length'])
        entered_code = self.rfile.read(content_length).decode('utf-8')

        # Check if the code is correct
        if check_code(entered_code):
            # Reset login attempts on successful login
            login_attempts = 0
            self.send_response(200)
            self.end_headers()
            with open('win.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            login_attempts += 1

            # If 3 attempts are reached, impose a timeout
            if login_attempts == 3:
                impose_timeout()
                login_attempts = 0
                self.send_response(400)
                self.end_headers()
                self.wfile.write("""
                    Too many incorrect attempts. Please wait for 30 seconds before trying again.
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
                """.encode())
            else:
                # If there are remaining attempts, show the message and also include JavaScript for automatic redirection
                time_remaining = int(10 - (time.time() - last_attempt_time))
                self.send_response(400)
                self.end_headers()
                self.wfile.write(f"""
                    Incorrect code.\nNote: A 30 seconds timeout will be imposed on 3 wrong attempts in a row.
                    <script>
                        var countdown = {time_remaining};
                        var countdownInterval = setInterval(function() {{
                            countdown -= 1;
                            document.getElementById('countdown').innerHTML = countdown;
                            if (countdown <= 0) {{
                                clearInterval(countdownInterval);
                                window.location.href = '/';
                            }}
                        }}, 1000);
                    </script>
                    <p>Redirecting in <span id='countdown'>{time_remaining}</span> seconds...</p>
                """.encode())

if __name__ == '__main__':
    # Set the IP address and port
    ip = '0.0.0.0'
    port = 8092

    # Change the working directory to where the HTML files are located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Create the server
    handler = MyHandler
    with socketserver.TCPServer((ip, port), handler) as httpd:
        print(f"Serving on {ip}:{port}")
        httpd.serve_forever()
