from aiohttp import web, ClientSession
import time
import asyncio
from aiohttp.web_exceptions import HTTPFound

app = web.Application()

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
async def home(request):
    return web.FileResponse('index.html')  # assuming index.html is in the same directory

# Route for handling code submission
async def check_code_route(request):
    global login_attempts

    # Check if a timeout is in effect
    if time.time() - last_attempt_time < 30:
        return web.Response(text="Too many attempts. Please wait for 30 seconds before trying again.")

    # Get the entered code from the form
    data = await request.post()
    entered_code = data.get('code')

    # Check if the code is correct
    if check_code(entered_code):
        # Reset login attempts on successful login
        login_attempts = 0
        return web.Response(text="You have successfully entered the correct code.")
    else:
        login_attempts += 1

        # If 3 attempts are reached, impose a timeout
        if login_attempts == 3:
            impose_timeout()
            login_attempts = 0
            return web.Response(text="Too many incorrect attempts. Please wait for 30 seconds before trying again.")

        return web.Response(text=f"Incorrect code. Attempts remaining: {3 - login_attempts}")

async def start_server():
    print("Starting Server")
    app.router.add_get("/", home)
    app.router.add_post("/check_code", check_code_route)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8089)
    await site.start()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server())
    loop.run_forever()
