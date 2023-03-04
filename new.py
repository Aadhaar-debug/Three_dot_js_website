import socket
import os

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5000
BUFFER_SIZE = 4096

def file_transfer(conn, addr):
    current_dir = os.getcwd()
    conn.send("Connected to the server. Enter the name of the file you want to download: ".encode())
    file_name = conn.recv(BUFFER_SIZE).decode()
    file_path = os.path.join(current_dir, file_name)
    if os.path.exists(file_path):
        conn.send(f"File {file_name} found. Sending file...".encode())
        with open(file_path, "rb") as f:
            data = f.read(BUFFER_SIZE)
            while data:
                conn.send(data)
                data = f.read(BUFFER_SIZE)
        conn.send("File sent successfully!".encode())
    else:
        conn.send(f"File {file_name} not found on the server.".encode())
    conn.close()

def start_server():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(1)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")
    while True:
        conn, addr = server_socket.accept()
        print(f"Client {addr[0]}:{addr[1]} connected")
        file_transfer(conn, addr)

if __name__ == "__main__":
    start_server()
