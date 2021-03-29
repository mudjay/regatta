import socket
from _thread import *
import pickle
#from game import Game

server = "192.168.0.102"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

maxFlotillaSize = 6
s.listen(maxFlotillaSize)
print("Waiting for a connection, Server Started")

# connected = set()
# games = {}
# idCount = 0
#
#
def threaded_client(conn):
    pass
    conn.send(str.encode("connected"))

    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode("utf-8")
            if not data:
                print("disconnected")
                break
            else:
                print("recieved: ", data)
            conn.sendall(str.encode(reply))
        except:
            break



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, ))