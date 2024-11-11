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
import sys


class ClientType(Enum):
     Console = 0
     Pygame = 1

client_type = ClientType.Pygame

def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py <parameter>")
        sys.exit(1)

    parameter = sys.argv[1]

    if parameter == 1:
        client_type = ClientType.Pygame
    elif parameter == 0:
        client_type = ClientType.Console

    # Do something with the parameter
    print("\n\n\nParameter:", parameter)
    print("\n\n\nClientType:", client_type)


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
