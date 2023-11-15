import socket
import threading
import random as rnd
import json

WIDTH, HEIGHT = 1000, 1000

class Player:
    def __init__(self):
        self.x = rnd.randint(0, WIDTH)
        self.y = rnd.randint(0, HEIGHT)
        self.speed = 1
        self.size = 50
        self.target = [rnd.randint(0, WIDTH), rnd.randint(0, HEIGHT)]

    def move(self, move_to_x, move_to_y):
        if move_to_x > self.x:
            self.x += self.speed
        elif move_to_x < self.x:
            self.x -= self.speed
        else:
            self.target[0] = rnd.randint(0, WIDTH)

        if move_to_y > self.y:
            self.y += self.speed
        elif move_to_y < self.y:
            self.y -= self.speed
        else:
            self.target[1] = rnd.randint(0, HEIGHT)

def handle_connection(client):
    print(client, 'connected')
    players[client] = Player()
    connected = True
    while connected:
        receiving_data = client.recv(2048).decode('utf-8')
        if receiving_data == 'disconnect':
            connected = False
            break
        players[client].move(*json.loads(receiving_data))
        client.send(json.dumps(get_all_player_positions()).encode('utf-8'))

    players.pop(client)
    client.close()

def accept_connections():
    while True:
        client, address = server.accept()
        players[client] = Player()
        thread = threading.Thread(target=handle_connection, args=(client,))
        thread.start()

def get_all_player_positions():
    return [(players[i].x, players[i].y) for i in players]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()), 5050))
server.listen()

players = {}

main_thread = threading.Thread(target=accept_connections, args=())
main_thread.start()

while True:
    all_player_positions = get_all_player_positions()
    # Your additional game logic here
