import pygame
from pygame.math import Vector2
import math


class Player():
    def __init__(self, x, y, player, color, radius, name, hp):
        self.name = name
        self.hp = hp
        self.pos = Vector2(x,y)
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)
        self.delay = 25
        self.max_vel = 10
        self.is_alive = True
        self.color = color
        self.radius = radius

        self.ammo = 7
        self.reloading = False
        self.bullets = []
        self.hits = []

    def draw(self, screen):
        if self.is_alive:
            self.hitbox = pygame.draw.rect(screen, (255, 0, 0), (self.pos.x - 20, self.pos.y - 20, 40, 40), 1)
            pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        else:
            pygame.draw.circle(screen, (0,0,0), (int(self.pos.x), int(self.pos.y)), self.radius)

    def set_hitbox(self, screen):
        self.hitbox = pygame.draw.rect(screen, (255, 0, 0), (self.pos.x - 20, self.pos.y - 20, 40, 40), 1)

    def got_hit(self):

        if self.hp > 0:
            self.hp -= 1
            print(f'{self.name} {self.hp}/10hp')
            if self.hp <= 0:
                self.is_alive = False
                print(f'{self.name} is dead')


    def tick(self):
        if self.delay > 0:
            self.delay -= 1



    def move(self, game):
        keys = pygame.key.get_pressed()
        event = pygame.mouse.get_pressed()

        if self.is_alive:
            if self.reloading == False:
                if event[0] == 1 and self.delay == 0 and self.ammo > 0:
                    mouse_pos = pygame.mouse.get_pos()
                    if len(self.bullets) < 600:
                        bullet = Projectile(self.pos.x, self.pos.y, mouse_pos, self.name)
                        bullet.set_hitbox(game.screen)
                        self.bullets.append(bullet)
                        self.ammo -= 1

                    if self.ammo <= 0:
                        self.reloading = True
                        self.delay = 120
                    else:
                        self.delay = 25
            else:
                if self.delay == 0:
                    self.ammo = 7
                    self.reloading = False




            if keys[pygame.K_LEFT]:
                self.add_force(Vector2(-1,0))

            if keys[pygame.K_RIGHT]:
                self.add_force(Vector2(1,0))

            if keys[pygame.K_UP]:
                self.add_force(Vector2(0,-1))

            if keys[pygame.K_DOWN]:
                self.add_force(Vector2(0,1))

            self.vel *= 0.8

            if self.vel.length() < self.max_vel:
                self.vel += self.acc
                self.acc *= 0
            else:
                pass

            if self.vel != 0:
                self.update_pos(game)




    def add_force(self, force):
        self.acc += force

    def update_pos(self, game):

        nv = self.pos + self.vel
        x = nv.x
        y = nv.y
        colision = False

        if nv.x < 0 or nv.x > game.width:
            self.vel.x *= 0
        if nv.y < 0 or nv.y > game.height:
            self.vel.y *= 0



        for obs in game.obstacles:
            if x+self.radius >= obs.x1 and x-self.radius <= obs.x2 and y+self.radius >= obs.y1 and y-self.radius <= obs.y2:
                self.vel.x *= 0
                self.vel.y *= 0






        self.pos += self.vel


class Weapon():
    def __init__(self):
        pass


class Projectile():
    def __init__(self, x, y, mouse_pos, name):
        self.x = int(x)
        self.y = int(y)
        self.pos = Vector2(x, y)
        self.name = name
        self.width = 10
        self.height = 10
        self.direction = Vector2(x-mouse_pos[0]+0.001, y-mouse_pos[1]+0.001).normalize().rotate(180)
        self.vel = self.direction*10


    def tick(self):
        self.pos += self.vel


    def draw(self, screen):
        pygame.draw.circle(screen, (0,0,0), (int(self.pos.x), int(self.pos.y)), 5)
        self.hitbox = pygame.draw.rect(screen, (255,0,0), (self.pos.x-5, self.pos.y-5, self.width, self.height), 1)

    def draw_invi(self, screen):
        self.hitbox = pygame.draw.rect(screen, (0, 0, 255),(self.pos.x - 5, self.pos.y - 5, self.width, self.height), 1)

    def set_hitbox(self, screen):
        self.hitbox = pygame.draw.rect(screen, (255,0,0), (self.pos.x-5, self.pos.y-5, self.width, self.height), 1)



class Game():
    def __init__(self, width, height, name):
        self.name = name
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        self.bullets = []
        self.obstacles = []


class Obstacle():
    def __init__(self, x, y, width, height, color, screen):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height
        self.width = width
        self.height = height
        self.color = color
        self.screen = screen
        self.draw(self.screen)

    def draw(self, screen):
        self.hitbox = pygame.draw.rect(screen, (self.color), (self.x1, self.y1, self.width, self.height), 1)