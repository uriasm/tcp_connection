# -*- coding: utf-8 -*-
import socket
import os

HOST = os.getenv('TCP_SERVER_HOST', '127.0.0.1')
PORT = int(os.getenv('TCP_SERVER_PORT', 5000))


class TCPClient:
    """TCP client.

    This client connects to a specified TCP server, sends messages,
    and receives responses. It provides a basic interactive loop
    for sending and receiving text messages.
    """

    def __init__(self, host=HOST, port=PORT):
        """Initializes the TCPClient.

        Args:
            host (str, optional): The server hostname or IP address.
                Defaults to HOST.
            port (int, optional): The server port number.
                Defaults to PORT.
        """
        self.host = host
        self.port = port

    def start(self):
        """Starts the client interaction loop.

        Connects to the server and enters a loop to send and receive
        messages.  The loop continues until the user enters
        'DESCONEXION' or the connection is lost.
        """
        try:
            with socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((self.host, self.port))
                print(f"Connected to {self.host}:{self.port}")

                while True:
                    message = input(
                        "Enter a message ('DESCONEXION' to exit): ")
                    try:
                        client_socket.sendall(message.encode('utf-8'))
                    except (BrokenPipeError, ConnectionResetError):
                        print("Connection lost while sending data.")
                        break

                    if message.strip().upper() == "DESCONEXION":
                        print("Disconnecting...")
                        break

                    try:
                        response = client_socket.recv(1024)
                        if not response:
                            print("Server closed the connection.")
                            break
                        print(f"Server response: {response.decode('utf-8')}")
                    except (ConnectionResetError, OSError):
                        print("Connection lost while receiving data.")
                        break

        except ConnectionRefusedError:
            print(
                f"Could not connect to {self.host}:{self.port}. Is the server running?")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    client = TCPClient()
    client.start()
