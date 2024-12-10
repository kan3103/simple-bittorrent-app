import socket

def create_tcp_connection(ip, port):
  try:
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    s.connect((ip, port))
    
    print(f"Successfully connected to {ip}:{port}")
    
    # Close the connection
    s.close()
  except Exception as e:
    print(f"Failed to connect to {ip}:{port} - {e}")

if __name__ == "__main__":
  ip = "127.0.0.1"
  port = 8000
  create_tcp_connection(ip, port)