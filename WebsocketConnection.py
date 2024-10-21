"""
WebsocketConnection Module

This module contains the WebsocketConnection class (Console Manager)

Author: Christopher Pohl
Date: 2024-10-20
"""
import websocket
import threading
import queue

host_url = 'ws://localhost:3000'


# WebSocket handling
class WebsocketConnection:

    def __init__(self):
        self.game_data_queue = queue.Queue()
        self.ws_ready_event = threading.Event()
        self.ws = websocket.WebSocketApp(
            host_url,
            on_open=self.__on_open,
            on_message=self.__on_message,
            on_error=self.__on_error,
            on_close=self.__on_close,
            on_reconnect=self.__on_reconnect)

    def start_forever(self):
        self.ws.run_forever(ping_interval=30, ping_timeout=10)

    def __on_open(self, ws):
        print("Opened connection")
        self.ws_ready_event.set()

    def __on_error(self, ws, error):
        print(error)

    def __on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")
        print(f"Closed connection with status code: {close_status_code}, message: {close_msg}")

    def __on_message(self, ws, message):
        # log for debugging
        print(message)

        # Push the message into the thread safe queue
        self.game_data_queue.put(message)

    # Private method to determine if user method from console or gui is valid to be sent to server
    def __validate_user_message(self, message):
        valid = True
        if valid:
            return True
        else:
            return False

    def __on_reconnect(self, ws):
        print("### reconnected ###")

    def send_message(self, message):
        # Validate if message format is correct
        if self.__validate_user_message(message):
            self.ws.send(message)
        else:
            print("ERROR: Invalid message format")
            return
