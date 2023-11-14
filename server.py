import socket, threading, random as rnd, json

class players:
    players_list = []
    def __init__(self):
        self.x = rnd.randint(0, width)
        self.y = rnd.randint(0, height)
        self.speed = 1
        self.size = 50
        self.target = [rnd.randint(0, width), rnd.randint(0, height)]

    def move(self, move_to_x, move_to_y):
        if move_to_x > self.x:
            self.x += self.speed
        if move_to_x < self.x:
            self.x -= self.speed
        else:
            self.target[0] = rnd.randint(0, width)

        if move_to_y > self.y:
            self.y += self.speed
        if move_to_y < self.y:
            self.y -= self.speed
        else:
            self.target[1] = rnd.randint(0, height)


def handle_connection(client):
    clients[client] = players()
    while True:
        msg = client.recv(2048).decode('utf-8')
        clients[client].move(*json.loads(msg))
        client.send(json.dumps(all_player_positions).encode('utf-8'))
    

def accept_connections():
    while True:
        client, address = server.accept()
        clients[client] = 6
        thread = threading.Thread(target=handle_connection, args=(client,))

main_thread_1 = threading.Thread(target=accept_connections, args=())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((socket.gethostname(socket.gethostname), 5050))

server.listen()

clients = {}

width, height = 1000, 1000

while True:
    all_player_positions = [(clients[i].x, clients[i].y) for i in clients]