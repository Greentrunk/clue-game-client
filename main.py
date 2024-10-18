import websocket
import threading

ws = None
ws_ready_event = threading.Event()


def on_open(ws):
    print("Opened connection")
    ws_ready_event.set()


def on_error(ws, error):
    print(error)


def on_close(ws, close_status_code, close_msg):
    print("### closed ###")
    print(f"Closed connection with status code: {close_status_code}, message: {close_msg}")


def on_message(ws, message):
    print(message)

    # Probably would need to figure out what message type this is and update gui appropriately


def on_reconnect(ws):
    print("### reconnected ###")


# This will allow us to send messages free without blocking back to server
def send_messages():
    ws_ready_event.wait()  # Wait until WebSocket is open
    while True:
        message = input("Enter q to quit!\nEnter a message to send: \n")
        if ws:
            try:
                if message == "q":
                    ws.close()
                    break
                ws.send(message)
            except websocket.WebSocketConnectionClosedException:
                print("WebSocket connection is closed. Cannot send message.")
        else:
            print("WebSocket is not connected")


# WebSocket handling
def start_websocket():
    def on_message_wrapper(ws, message):
        on_message(ws, message)  # Pass to the actual message handler

    # websocket.enableTrace(True)
    global ws
    ws = websocket.WebSocketApp(
        "ws://localhost:3000",
        on_open=on_open,
        on_message=on_message_wrapper,
        on_error=on_error,
        on_close=on_close,
        on_reconnect=on_reconnect
    )
    ws.run_forever(ping_interval=30, ping_timeout=10)


if __name__ == "__main__":
    # main thread  manages user input, GUI (console, tkinter, pygame, etc.)

    # new thread that spawns connection
    websocket_thread = threading.Thread(target=start_websocket)
    websocket_thread.start()

    send_messages()
