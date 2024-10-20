"""
WebsocketConnection Module

This module contains the WebsocketConnection class

Author: Christopher Pohl
Date: 2024-10-20
"""
import websocket
import threading

host_url = 'ws://localhost:3000'


# WebSocket handling
class WebsocketConnection:

    def __init__(self):
        self.game_state_queue = None
        self.ws_ready_event = threading.Event()
        self.ws = websocket.WebSocketApp(
            host_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_reconnect=self.on_reconnect)


    def set_game_state_queue(self, queue):
        self.game_state_queue = queue

    def start_forever(self):
        self.ws.run_forever(ping_interval=30, ping_timeout=10)

    def on_open(self, ws):
        print("Opened connection")
        self.ws_ready_event.set()

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        print("### closed ###")
        print(f"Closed connection with status code: {close_status_code}, message: {close_msg}")

    def on_message(self, ws, message):
        # log for debugging
        print(message)

        # Push the message into the thread safe queue
        self.game_state_queue.put(message)

    def on_reconnect(self, ws):
        print("### reconnected ###")
