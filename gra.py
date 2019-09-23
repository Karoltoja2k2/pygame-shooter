import pygame
import sys
import math
from pygame.math import Vector2
import datetime
from network import Network
from tkinter import *
from objects import Player, Game, Projectile, Weapon, Obstacle


bg = pygame.image.load('bg.jpg')


def distance(players, host):

    visible_enemies = []
    invisible_enemies = []

    for player in players:
        if round(Vector2(player.pos.x-host.pos.x, player.pos.y-host.pos.y).length()) < 300:
            visible_enemies += [player]
        else:
            invisible_enemies += [player]

    return visible_enemies, invisible_enemies


def redrawWindow(host, visible_enemies, invisible_enemies):
    game.screen.fill((114,206,72))

    for obs in game.obstacles:
        obs.draw(game.screen)

    players = visible_enemies + invisible_enemies
    game.bullets = []
    host.hits = []

    for player in players:
        if player in visible_enemies:

            player.draw(game.screen)
        game.bullets += player.bullets


    host.draw(game.screen)

    for bullet in game.bullets:
        x = bullet.pos.x
        y = bullet.pos.y

        for obs in game.obstacles:
            if bullet.hitbox.colliderect(obs.hitbox):
                game.bullets.remove(bullet)

        if game.width > x > 0 and game.height > y > 0:
            if round(Vector2(x - host.pos.x, y - host.pos.y).length()) < 300:
                bullet.draw(game.screen)
            else:
                bullet.draw_invi(game.screen)
        else:
            game.bullets.remove(bullet)

    for bullet in host.bullets:
        x = bullet.pos.x
        y = bullet.pos.y

        for obs in game.obstacles:
            if bullet.hitbox.colliderect(obs.hitbox):
                host.bullets.remove(bullet)

        if game.width > x > 0 and game.height > y > 0:
            if round(Vector2(x - host.pos.x, y - host.pos.y).length()) < 300:
                bullet.draw(game.screen)
            else:
                bullet.draw_invi(game.screen)
        else:
            host.bullets.remove(bullet)

        for player in players:
            if bullet.hitbox.colliderect(player.hitbox):
                print(f'player {player.name} hit by {bullet.name}')
                host.hits += [player.name]
                print(host.hits)
                host.bullets.remove(bullet)

    pygame.display.update()

def connect(event):
    global data
    data = (name.get(), ip.get(), color.get())
    menu.destroy()

menu = Tk()

name = Entry(menu)
name_lab = Label(menu, text='Nick')

ip = Entry(menu)
ip_lab = Label(menu, text='Server ip')

color = Entry(menu)
color_lab = Label(menu, text='Color red/green/blue')


confirm = Button(menu, text='Continue', fg='green')
confirm.bind("<Button-1>", connect)


name_lab.grid(row=0, column=0)
name.grid(row=0, column=1)
ip_lab.grid(row=1, column=0)
ip.grid(row=1, column=1)
color_lab.grid(row=2, column=0)
color.grid(row=2, column=1)

confirm.grid(row=3, columnspan=2)


menu.mainloop()


width = 1280
height = 720


name = str(data[0])
ip = str(data[1])
color = str(data[2])





game = Game(width, height, name)



def run():
    run = True
    clock = pygame.time.Clock()

    n = Network(ip)


    host = n.connect(name, color)


    host.set_hitbox(game.screen)


    wall_left = Obstacle(0.1*width, 0.2*height, 5, 0.6*height, (0,0,0), game.screen)
    wall_right = Obstacle(0.9*width, 0.2*height, 5, 0.6*height, (0,0,0), game.screen)
    wall_mid_top = Obstacle(0.5*width, 0.1*height, 5, 0.3*height, (0,0,0), game.screen)
    wall_mid_bot = Obstacle(0.5*width, 0.6*height, 5, 0.3*height, (0, 0, 0), game.screen)

    game.obstacles += [wall_left, wall_right, wall_mid_top, wall_mid_bot]





    while run:
        clock.tick(60)
        host.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()


        for bullet in host.bullets:
            bullet.tick()

        host.move(game)

        players = n.send(host)


        for player in players:
            if player.name == game.name:
                host = player
                players.remove(player)
                break

        visible_enemies, invisible_enemies = distance(players, host)
        redrawWindow(host, visible_enemies, invisible_enemies)

run()






