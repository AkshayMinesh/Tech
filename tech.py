from flask import Flask, render_template, request, redirect, url_for
import time

app = Flask(__name__)

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

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling code submission
@app.route('/check_code', methods=['POST'])
def check_code_route():
    global login_attempts

    # Check if a timeout is in effect
    if time.time() - last_attempt_time < 30:
        return "Too many attempts. Please wait for 30 seconds before trying again."

    # Get the entered code from the form
    entered_code = request.form.get('code')

    # Check if the code is correct
    if check_code(entered_code):
        # Reset login attempts on successful login
        login_attempts = 0
        return "You have successfully entered the correct code."
    else:
        login_attempts += 1

        # If 3 attempts are reached, impose a timeout
        if login_attempts == 3:
            impose_timeout()
            login_attempts = 0
            return "Too many incorrect attempts. Please wait for 30 seconds before trying again."

        return f"Incorrect code. Attempts remaining: {3 - login_attempts}"

if __name__ == '__main__':
    app.run(host='4.193.160.83', port=8088, debug=True)

