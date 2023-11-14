import pygame as pg, random as rnd, sockets, json, socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((socket.gethostname(socket.gethostname), 5050))

def draw(*args):
    for player_pos in args:
        pg.draw.circle(window, (0, 50, 200), player_pos, player_size)

pg.init()
width, height = 1000, 1000
window = pg.display.set_mode((width, height))
clock = pg.time.Clock()
player_size = 50

running = True
while running:
    clock.tick(0)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()


    data = pg.mouse.get_pos()
    client.send(data.encode('utf-8'))
    player_poses = client.recv(2048).decode('utf-8')

    window.fill('black')
    draw(*player_poses)   
    pg.display.update()

