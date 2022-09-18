import socket

HOST = ""
PORT = 8001
BUFFER_SIZE = 4096

cmd = "GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(cmd.encode())
s.shutdown(socket.SHUT_WR)
responseFromProxy = s.recv(BUFFER_SIZE)
print(responseFromProxy)
s.close()