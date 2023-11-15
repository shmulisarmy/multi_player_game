import socket
import threading
import random as rnd
import json

WIDTH, HEIGHT = 1500, 1000

class Player:
    def __init__(self):
        self.x = rnd.randint(0, WIDTH)
        self.y = rnd.randint(0, HEIGHT)
        self.speed = 1
        self.size = 50
        self.target = [rnd.randint(0, WIDTH), rnd.randint(0, HEIGHT)]

    def move(self, move_to_x, move_to_y):
        if move_to_x > WIDTH/2:
            self.x += self.speed
        elif move_to_x < WIDTH/2:
            self.x -= self.speed
        else:
            self.target[0] = rnd.randint(0, WIDTH)

        if move_to_y > HEIGHT/2:
            self.y += self.speed
        elif move_to_y < HEIGHT/2:
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
        sending_data = (all_player_positions, (players[client].x - WIDTH/2, players[client].y - HEIGHT/2))
        client.send(json.dumps(sending_data).encode('utf-8'))

    players.popitem(client)
    client.close()

def accept_connections():
    while True:
        client, address = server.accept()
        players[client] = Player()
        thread = threading.Thread(target=handle_connection, args=(client,))
        thread.start()

def get_all_player_positions():
    print(len(players))
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
