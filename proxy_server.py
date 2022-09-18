import socket
from multiprocessing import Process
from echo_server import BUFFER_SIZE

# details for this server
ADDR = "" # Localhost
PORT = 8001
BUFFER_SIZE = 4096

# address to proxy
PROXY_ADDR = "www.google.com"
PROXY_PORT = 80

def startAnotherProcess(conn):
    proxy_outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect
    proxy_outgoing.connect((PROXY_ADDR, PROXY_PORT))
    # Do the proxy
    requestToProxy = conn.recv(BUFFER_SIZE)
    proxy_outgoing.sendall(requestToProxy)
    # Shutdown
    proxy_outgoing.shutdown(socket.SHUT_WR)
    # Get the response
    proxyedResponse = proxy_outgoing.recv(BUFFER_SIZE)
    # Send it back to the orignal connect
    conn.send(proxyedResponse)
    # close
    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_incoming:
    
    proxy_incoming.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_incoming.bind((ADDR, PORT))
    proxy_incoming.listen(1)

    # Listen loop
    while True:
        conn, addr = proxy_incoming.accept()
        p = Process(target=startAnotherProcess, args=(conn,))
        p.daemon = True
        p.start()
        print("Process with ID: ", p, " started!")



