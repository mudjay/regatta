import socket
from _thread import *
import pickle
from game import *
from common import Message

roomCounter = 0
connCounter = 0
connLookup = {}
lobby = []
rooms = []


class Client:
    def __init__(self, connection, clientID):
        self.connection = connection
        self.clientID = clientID
        self.room = None

    def send(self, mess):
        self.connection.sendall(pickle.dumps(mess))


class Umpire(Client):
    def __init__(self, connection, clientID):
        super().__init__(connection, clientID)



    def handle_message(self, mess):
        def make_room():
            global rooms, roomCounter
            mapPath, name = mess.data
            rooms.append(Room(self, mapPath, roomCounter, name=name))
            roomCounter += 1
            print(rooms)

        switchType = {'make': make_room}
        switchType[mess.messageType]()

class Viewer(Client):
    def __init__(self, connection, clientID):
        super().__init__(connection, clientID)
        self.boat = None

    def handle_message(self, mess):
        def handle_get():
            switch = {'mapPath': self.room.mapPath,
                      'boats':  [boat.get_attr() for boat in self.room.game.flotilla],
                      'buoys': [buoy.get_attr() for buoy in self.room.game.buoys],
                      'wind': self.room.game.wind
                      }
            reply = Message('give', switch[mess.data])
            self.send(reply)

        def handle_join():
            room = find_room(mess.data)
            room.join(self)


        switchType = {'get': handle_get,
                      'join': handle_join,
                      # 'move': handle_move,
                      }
        switchType[mess.messageType]()


class Player(Client):
    def __init__(self, connection, clientID):
        super().__init__(connection, clientID)
        self.room = None

    def handle_message(self, mess):
        def handle_get():
            # switch = {'rooms': [[room.roomID, room.name] for room in rooms],
            #           'colours': [boat.get_colour() for boat in self.room.game.flotilla],
            #           'moves': self.room.game.find_in_flotilla(self.clientID).get_valid_moves(),
            #           'wind': self.room.game.wind
            #           }

            # really ugly solution: with above could not create the dict when not every option was valid
            # below tries to create each option and passes if couldn't, at four times the length :/
            # at this point it is probably better to use a block of if, elifs
            switch = {}
            try:
                switch.update({'rooms': [[room.roomID, room.name] for room in rooms]})
            except:
                pass
            try:
                switch.update({'colours': [[boat.boatID, boat.get_colour()] for boat in self.room.game.flotilla]})
            except:
                pass
            try:
                switch.update({'moves': self.room.game.find_in_flotilla(self.clientID).get_valid_moves()})
            except:
                pass
            try:
                switch.update({'wind': self.room.game.wind})
            except:
                pass

            reply = Message('give', switch[mess.data])
            self.send(reply)

        def handle_move():
            pass

        def handle_join():
            room = find_room(mess.data)
            room.join(self)
            self.room = room    # is this circular? would it make more sense just to show room in one place?

        switchType = {'get': handle_get,
                      'join': handle_join,
                      'move': handle_move,
                      }
        switchType[mess.messageType]()


def start_server():
    server = "192.168.0.102"
    port = 5555
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((server, port))
        print("server started")
    except socket.error as e:
        print(e)
    sock.listen(5)

    return sock


def find_room(roomID):
    for room in rooms:
        if room.roomID == roomID:
            return room
    return None


def threaded_client(connection, connectionID):
    connection.sendall(pickle.dumps([True, connectionID]))
    identified = False
    client = None
    while not identified:
        try:
            message = pickle.loads(connection.recv(2048))
            if not message:
                break
            else:
                if message.messageType == 'id':
                    switch = {'player': Player(connection, connectionID),
                              'viewer': Viewer(connection, connectionID),
                              'umpire': Umpire(connection, connectionID)
                              }
                    client = switch[message.data]
                    identified = True
                    print(identified, client.__class__.__name__)
        except Exception as e:
            print(e)
            break
    while True:
        try:
            message = pickle.loads(connection.recv(2048*4))
            if not message:
                break
            else:
                message.print()
                client.handle_message(message)
        except Exception as e:
            print(e)
            break

    print("Lost connection")
    try:
        if client.__class__.__name__ == 'Umpire':
            # delete the room they started
            pass
        del client
    except Exception as e:
        print(e)
    connection.close()
    del connLookup[connectionID]


##########################################################################
s = start_server()
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    start_new_thread(threaded_client, (conn, connCounter))
    connLookup.update({connCounter: conn})
    connCounter += 1
