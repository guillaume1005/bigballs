# Echo client program
import socket
import sys

HOST = ""  # The remote host
PORT = 50007  # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(sys.argv[1])
data = s.recv(1024)
s.close()
print("Received", repr(data))

# facilitate imports
