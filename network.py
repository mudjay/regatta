import socket
import pickle
from common import Message

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.102"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connected = False

    def connect(self):
        try:
            self.client.connect(self.addr)
            self.connected, clientID = pickle.loads(self.client.recv(2048))
            return clientID
        except Exception as e:
            print(e)

    def send(self, messType, data):
        try:
            self.client.sendall(pickle.dumps(Message(messType, data)))
            if messType == 'get':
                return pickle.loads(self.client.recv(2048*4)).read()
            # send a confirmation? is this all handled by sendall?
        except socket.error as e:
            print(e)
