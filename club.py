from aiohttp import web, ClientSession
import time
import asyncio
from aiohttp.web_exceptions import HTTPFound
import aiohttp
import os 

login_attempts = 0
last_attempt_time = 0

app = web.Application()
# Function to check if the code is correct
def check_code(code):
    return code in correct_codes

# Function to impose a timeout after 3 failed attempts
def impose_timeout():
    global last_attempt_time
    last_attempt_time = time.time()

async def protected_handler(request):
    global login_attempts

    # Check if a timeout is in effect
    if time.time() - last_attempt_time < 30:
        time_remaining = int(30 - (time.time() - last_attempt_time))
        return web.Response(
            text=f"Too many attempts. Please wait for {time_remaining} seconds before trying again.",
            status=400
        )

    # Get the entered code from the form
    entered_code = await request.text()

    # Check if the code is correct
    if check_code(entered_code):
        # Reset login attempts on successful login
        login_attempts = 0
        return web.FileResponse('win.html')  # Render the win template

    else:
        login_attempts += 1

        # If 3 attempts are reached, impose a timeout
        if login_attempts == 3:
            impose_timeout()
            login_attempts = 0
            return web.Response(
                text=f"Too many incorrect attempts. Please wait for 30 seconds before trying again."
                     f"<script>"
                     f"var countdown = 30;"
                     f"var countdownInterval = setInterval(function() {{"
                     f"countdown -= 1;"
                     f"document.getElementById('countdown').innerHTML = countdown;"
                     f"if (countdown <= 0) {{"
                     f"clearInterval(countdownInterval);"
                     f"window.location.href = '/';"
                     f"}}"
                     f"}}, 1000);"
                     f"</script>"
                     f"<p>Redirecting in <span id='countdown'>30</span> seconds...</p>",
                status=400
            )
        else:
            # If there are remaining attempts, show the message and also include JavaScript for automatic redirection
            time_remaining = int(10 - (time.time() - last_attempt_time))
            return web.Response(
                text=f"Incorrect code.\nNote: A 30 seconds timeout will be imposed on 3 wrong attempts in a row."
                     f"<script>"
                     f"var countdown = {time_remaining};"
                     f"var countdownInterval = setInterval(function() {{"
                     f"countdown -= 1;"
                     f"document.getElementById('countdown').innerHTML = countdown;"
                     f"if (countdown <= 0) {{"
                     f"clearInterval(countdownInterval);"
                     f"window.location.href = '/';"
                     f"}}"
                     f"}}, 1000);"
                     f"</script>"
                     f"<p>Redirecting in <span id='countdown'>{time_remaining}</span> seconds...</p>",
                status=400
            )


async def start_server():
    global aiosession
    print("Starting Server")

    app.router.add_get("/", protected_handler)

    aiosession = aiohttp.ClientSession()
    server = web.AppRunner(app)

    await server.setup()
    print("Server Started")
    await web.TCPSite(server, port=8093).start()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_forever(start_server())
