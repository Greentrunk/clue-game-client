"""
Entry Point

This is the entry point to the Clue-less client.

Author: Christopher Pohl
Date: 2024-10-20
"""
import threading
from WebsocketConnection import WebsocketConnection
from GUI import GUI
from enum import Enum
from Console import Console


class ClientType(Enum):
    Console = 0
    Pygame = 1


client_type = ClientType.Pygame

if __name__ == "__main__":
    websocket_connection = WebsocketConnection()

    # new thread that spawns connection
    websocket_thread = threading.Thread(target=websocket_connection.start_forever)
    websocket_thread.start()

    if client_type == ClientType.Console:
        console = Console(websocket_connection.ws, websocket_connection.game_data_queue)
        console.run()
    else:
        gui = GUI(websocket_connection.ws, websocket_connection.game_data_queue)
        gui.run()
