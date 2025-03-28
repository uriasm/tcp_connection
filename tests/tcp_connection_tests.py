# -*- coding: utf-8 -*-
import socket
import threading

import pytest
from tcp_server import TCPServer, HOST, PORT


# Define a fixture for setting up a test server
@pytest.fixture
def test_server():
    return TCPServer(host=HOST, port=PORT + 1)


# Test cases for TCPServer.start()
@pytest.mark.parametrize(
    "message, expected_response",
    [
        ("hello", "HELLO"),  # Basic uppercase echo
        ("Hola Server", "Hola Cliente"),  # Specific greeting
        ("DESCONEXION", ""),  # Disconnection message
        ("", ""),  # Empty message
        ("   leading and trailing spaces   ",
         "   LEADING AND TRAILING SPACES   "),  # Whitespace handling
        ("MixedCase", "MIXEDCASE"),  # Mixed case handling
        ("12345", "12345"),  # Numeric input
        ("~!@#$%^&*()_+=-`", "~!@#$%^&*()_+=-`"),  # Special characters
    ],
    ids=[
        "basic_uppercase",
        "specific_greeting",
        "disconnection",
        "empty_message",
        "whitespace_handling",
        "mixed_case",
        "numeric_input",
        "special_characters",
    ],
)
def test_start_message_handling(test_server, message, expected_response):
    # Arrange
    server = test_server

    # Start the server in a separate thread
    import threading
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()

    # Act
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server.host, server.port))
        client_socket.sendall(message.encode('utf-8'))
        if expected_response:
            response = client_socket.recv(1024).decode('utf-8')
        else:
            response = ""

    # Assert
    assert response == expected_response


# Test cases for TCPServer.__init__()
@pytest.mark.parametrize(
    "host, port",
    [
        (HOST, PORT + 2),  # Default host and custom port
        ("localhost", PORT + 3),  # Custom host and port
    ],
    ids=[
        "default_host_custom_port",
        "custom_host_and_port",
    ],
)
def test_init(host, port):
    # Act
    server = TCPServer(host=host, port=port)

    # Assert
    assert server.host == host
    assert server.port == port


# Test case for handling client disconnect
def test_client_disconnect(test_server):
    # Arrange
    server = test_server
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()

    # Act
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server.host, server.port))
        client_socket.shutdown(socket.SHUT_RDWR)  # Simulate client disconnect
        client_socket.close()
