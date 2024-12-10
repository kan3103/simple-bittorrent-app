import socket


def runserver():
  # Create a socket object
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  
  # Bind the socket to an address and port
  s.bind(("0.0.0.0", 8000))

  # Listen for incoming connections
  s.listen(5)
  hostname = socket.gethostname()
  local_ip = socket.gethostbyname(hostname)
  print(f"Listening on {local_ip}, port {s.getsockname()[1]}")
  while True:
    # Accept a connection
    client_socket, addr = s.accept()
    print(f"Connection from {addr}")
    
    # Send a message to the client
    client_socket.send(b"Hello, client!")
    
    # Close the connection
    client_socket.close()


if __name__ == "__main__":
  runserver()