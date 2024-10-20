import websocket
import threading
import json

ws = None
ws_ready_event = threading.Event()

def on_open(ws):
    print("Opened connection")
    ws_ready_event.set()

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print(f"Closed connection with status code: {close_status_code}, message: {close_msg}")

def on_message(ws, message):
    try:
        # Parse incoming message and extract game state
        game_data = json.loads(message)
        if 'game_state' in game_data:
            print("Current Game State:", json.dumps(game_data['game_state'], indent=4))
        else:
            print(f"Received: {message}")
    except json.JSONDecodeError:
        print(f"Non-JSON message received: {message}")

# WebSocket handling
def start_websocket():
    global ws
    ws = websocket.WebSocketApp(
        "ws://localhost:3000",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever(ping_interval=30, ping_timeout=10)

if __name__ == "__main__":
    # Start a new thread for WebSocket connection
    websocket_thread = threading.Thread(target=start_websocket)
    websocket_thread.start()
