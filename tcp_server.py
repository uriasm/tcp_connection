# -*- coding: utf-8 -*-
import os
import socket
import logging
import threading

# --- Configuration ---
HOST = os.getenv('TCP_SERVER_HOST', '127.0.0.1')
PORT = int(os.getenv('TCP_SERVER_PORT', 5000))
TIMEOUT = int(os.getenv('TCP_SERVER_TIMEOUT', 10))  # seconds

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("tcp_server.log"),
        logging.StreamHandler()
    ]
)


class TCPServer:
    """TCP server.
    This server listens for incoming connections, receives messages,
    and sends responses. It handles 'DESCONEXION' messages for
    client disconnections and responds to "hola server" with
    "Hola Cliente".  Other messages are simply echoed back in
    uppercase.
    """

    def __init__(self, host=HOST, port=PORT):
        """Initializes the TCPServer.

        Args:
            host (str, optional): The server hostname or IP address.
                Defaults to HOST.
            port (int, optional): The server port number.
                Defaults to PORT.
        """
        self.host = host
        self.port = port

    def start(self):
        """Starts the server.

        Binds to the specified host and port, listens for connections,
        and handles incoming messages. The server echoes back received
        messages in uppercase, unless the message is "hola server",
        in which case it responds with "Hola Cliente".  The server
        also handles "DESCONEXION" messages to gracefully close
        client connections.
        """
        try:
            with socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.bind((self.host, self.port))
                server_socket.listen()
                server_socket.settimeout(TIMEOUT)
                logging.info(f"Server listening on {self.host}:{self.port}...")

                while True:
                    try:
                        conn, addr = server_socket.accept()
                        logging.info(f"Connection established from {addr}")

                        # Launch a new thread for each client
                        client_thread = threading.Thread(
                            target=self.handle_client, args=(conn, addr),
                            daemon=True)
                        client_thread.start()

                    except socket.timeout:
                        logging.warning(
                            "Socket accept() timeout — no connection within "
                            "timeout.")
                        continue
                    except Exception as e:
                        logging.error(
                            f"Error accepting client: {e}", exc_info=True)

        except OSError as e:
            logging.critical(
                f"Failed to bind/listen on {self.host}:{self.port}: {e}",
                exc_info=True)
        except Exception as e:
            logging.critical(f"Unexpected server error: {e}", exc_info=True)

    def handle_client(self, conn, addr):
        """Handles a client connection.

        Receives data from the client, processes it, and sends back a
        response.  Handles "DESCONEXION" messages for disconnection
        and specific greetings.

        Args:
            conn (socket.socket): The client socket.
            addr (tuple): The client's address.
        """
        try:
            with conn:
                while True:
                    try:
                        data = conn.recv(1024).decode('utf-8')
                        if not data:
                            break
                        logging.info(f"Message received from {addr}: {data}")

                        if data.strip().upper() == "DESCONEXION":
                            logging.info(
                                f"Client {addr} requested DESCONEXION.")
                            break

                        if data.strip().lower() == "hola server":
                            response = "Hola Cliente"
                        else:
                            response = data.upper()

                        conn.sendall(response.encode('utf-8'))

                    except socket.timeout:
                        logging.warning(
                            f"Connection with {addr} timed out after {TIMEOUT} seconds.")
                        break
                    except (ConnectionResetError, TimeoutError) as net_err:
                        logging.warning(
                            f"Connection error with {addr}: {net_err}")
                        break
                    except Exception as e:
                        logging.error(
                            f"Unexpected error handling client {addr}: {e}",
                            exc_info=True)
                        break

        finally:
            logging.info(f"Connection with {addr} closed.")


if __name__ == "__main__":
    server = TCPServer()
    server.start()
