from fastapi import FastAPI
import requests
import time
import threading

app = FastAPI()

# Default pong time in milliseconds
pong_time_ms = 1000

# Flag to control whether the game is running
is_running = False

# The URL of the other server instance
instance_url = None

@app.post("/start/{delay}")
def start_game(delay: int, instance_url_param: str):
    """
    Starts the ping-pong game by setting the delay and the other instance's URL.
    A separate thread is started to handle sending ping requests.
    
    Args:
        delay (int): The time interval between pings in milliseconds.
        instance_url_param (str): The URL of the other server instance.
    
    Returns:
        dict: A message indicating that the game has started and the pong time.
    """
    global is_running, pong_time_ms, instance_url
    pong_time_ms = delay
    instance_url = instance_url_param
    is_running = True
    # Start a new thread to send ping requests
    threading.Thread(target=send_ping).start()
    return {"message": "Game started", "pong_time_ms": pong_time_ms}

@app.post("/pause")
def pause_game():
    """
    Pauses the ping-pong game by setting the running flag to False.
    
    Returns:
        dict: A message indicating that the game has been paused.
    """
    global is_running
    is_running = False
    return {"message": "Game paused"}

@app.post("/resume")
def resume_game():
    """
    Resumes the ping-pong game by restarting the ping thread.
    
    Returns:
        dict: A message indicating that the game has resumed.
    """
    global is_running
    is_running = True
    # Start a new thread to resume sending ping requests
    threading.Thread(target=send_ping).start()
    return {"message": "Game resumed"}

@app.post("/stop")
def stop_game():
    """
    Stops the ping-pong game by setting the running flag to False.
    
    Returns:
        dict: A message indicating that the game has been stopped.
    """
    global is_running
    is_running = False
    return {"message": "Game stopped"}

@app.get("/ping")
def ping():
    """
    Responds to a ping request with a pong message.
    
    Returns:
        dict: A message indicating a "pong" response.
    """
    return {"message": "pong"}

def send_ping():
    """
    Continuously sends ping requests to the other server instance
    while the game is running. It waits for the specified delay
    before each ping. If a request fails, it stops sending pings.
    """
    global is_running
    while is_running:
        # Wait for the specified delay (convert ms to seconds)
        time.sleep(pong_time_ms / 1000.0)
        try:
            # Send a GET request to the other instance's /ping endpoint
            response = requests.get(f"{instance_url}/ping")
            if response.status_code == 200:
                print("Received pong from:", instance_url)
        except Exception as e:
            print("Failed to send ping:", str(e))
            break
