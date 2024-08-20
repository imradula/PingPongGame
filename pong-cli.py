import sys
import requests

# URLs for the two server instances
server1_url = "http://127.0.0.1:8000"
server2_url = "http://127.0.0.1:8001"

def start_game(pong_time_ms):
    """
    Starts the pong game by sending a start request to both server instances.
    
    Args:
        pong_time_ms (int): The time interval between pings in milliseconds.
    """
    try:
        # Start the game on both servers, passing the URL of the other instance
        requests.post(f"{server1_url}/start/{pong_time_ms}", params={"instance_url_param": server2_url})
        requests.post(f"{server2_url}/start/{pong_time_ms}", params={"instance_url_param": server1_url})
        print(f"Started game with {pong_time_ms}ms delay")
    except Exception as e:
        print("Error starting game:", e)

def pause_game():
    """
    Pauses the pong game by sending a pause request to both server instances.
    """
    try:
        # Send a pause command to both servers
        requests.post(f"{server1_url}/pause")
        requests.post(f"{server2_url}/pause")
        print("Paused game")
    except Exception as e:
        print("Error pausing game:", e)

def resume_game():
    """
    Resumes the pong game by sending a resume request to both server instances.
    """
    try:
        # Send a resume command to both servers
        requests.post(f"{server1_url}/resume")
        requests.post(f"{server2_url}/resume")
        print("Resumed game")
    except Exception as e:
        print("Error resuming game:", e)

def stop_game():
    """
    Stops the pong game by sending a stop request to both server instances.
    """
    try:
        # Send a stop command to both servers
        requests.post(f"{server1_url}/stop")
        requests.post(f"{server2_url}/stop")
        print("Stopped game")
    except Exception as e:
        print("Error stopping game:", e)

if __name__ == "__main__":
    # Ensure that the command and parameters are passed correctly
    if len(sys.argv) < 2:
        print("Usage: python pong-cli.py <command> <param>")
        sys.exit(1)

    command = sys.argv[1]

    # Handle the different CLI commands: start, pause, resume, stop
    if command == "start" and len(sys.argv) == 3:
        pong_time_ms = int(sys.argv[2])
        start_game(pong_time_ms)
    elif command == "pause":
        pause_game()
    elif command == "resume":
        resume_game()
    elif command == "stop":
        stop_game()
    else:
        # Print an error message if the command is invalid or parameters are missing
        print("Invalid command or missing parameters")
