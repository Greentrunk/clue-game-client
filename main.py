import threading
from WebsocketConnection import WebsocketConnection
from GUI import GUI

# This will allow us to send messages free without blocking back to server
# def send_messages():
#     ws_ready_event.wait()  # Wait until WebSocket is open
#     while True:
#         message = input("Enter q to quit!\nEnter a message to send: \n")
#         if ws:
#             try:
#                 if message == "q":
#                     ws.close()
#                     break
#                 ws.send(message)
#             except websocket.WebSocketConnectionClosedException:
#                 print("WebSocket connection is closed. Cannot send message.")
#         else:
#             print("WebSocket is not connected")


if __name__ == "__main__":
    websocket_connection = WebsocketConnection()
    gui = GUI(websocket_connection.ws)

    # helps sync messages between pygame and our websocket connection
    websocket_connection.set_game_state_queue(gui.game_data_queue)

    # new thread that spawns connection
    websocket_thread = threading.Thread(target=websocket_connection.start_forever)
    websocket_thread.start()

    gui.run()
