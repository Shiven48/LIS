# import socket

# HOST = '192.168.88.204'  # IP of the machine
# PORT = 5600              # Port the machine sends data to

# def listen_to_erba():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind(('', PORT))  # Bind to all local interfaces on given port
#         s.listen()
#         print(f"Listening on port {PORT}...")

#         conn, addr = s.accept()
#         with conn:
#             print(f"Connected by {addr}")
#             data = b""
#             while True:
#                 chunk = conn.recv(1024)
#                 if not chunk:
#                     break
#                 data += chunk

#             print("Raw Data Received:")
#             print(data.decode(errors="ignore"))  # decode with ignore in case of non-UTF characters


# if __name__ == "__main__":
#     listen_to_erba()