import pygame as pg
import json
import socket

def draw(*args):
    for player_pos in args:
        pg.draw.circle(window, (0, 50, 200), (player_pos[0] - offset[0], player_pos[1] - offset[1]), player_size)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostbyname(socket.gethostname()), 5050))

width, height = 1500, 1000
window = pg.display.set_mode((width, height))
clock = pg.time.Clock()
player_size = 50
pg.init()

running = True
try:
    while running:
        clock.tick(60)  # Adjust the frames per second as needed

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        sending_data = json.dumps(pg.mouse.get_pos())
        client.send(sending_data.encode('utf-8'))
        try:
            player_poses, offset = json.loads(client.recv(2048).decode('utf-8'))
            print(offset)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            player_poses = []

        window.fill('grey')
        for i in range(-50, width, 25):
            pg.draw.line(window, (0,0,0), (i - offset[0]%25, offset[1]%25), (i - offset[0]%25, height - offset[1]%25), 1)
        for i in range(-50, height, 25):
            pg.draw.line(window, (0,0,0), (offset[0]%25, i - offset[1]%25), (width - offset[0]%25, i - offset[1]%25), 1)
        draw(*player_poses)
        pg.display.update()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client.send('disconnect'.encode('utf-8'))
    client.close()
    pg.quit()
