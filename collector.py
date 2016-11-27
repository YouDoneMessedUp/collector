import pygame
from pygame.locals import *
import time
import random
from time import time
import math

pygame.font.init()
myfont = pygame.font.SysFont("mirc", 25)

screen = pygame.display.set_mode((720, 480))
clock = pygame.time.Clock()

seconds = 0
speed = 2
Yspeed = speed*1.7

helmets = 0
chestplates = 0
necklaces = 0
leggings = 0
watches = 0

pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

done = False
black = (0, 0, 0)

keys = {"w":False, "a":False, "s":False, "d":False, " ":False, "q":False}

class Thing:
    def __init__(self, picture, pos):
        self.texture = pygame.image.load(picture).convert()
        self.position = pos
        
    def draw(self, screen):
        screen.blit(self.texture, tuple([int(e) for e in self.position]))

    def iscolliding(self, other):
        size = self.texture.get_size()
        othersize = other.texture.get_size()
        if self.position[0] <= other.position[0]+othersize[0] and self.position[0]+size[0] >= other.position[0]:
            if self.position[1] <= other.position[1]+othersize[1] and self.position[1]+size[1] >= other.position[1]:
                return True
        return False

    def move_random(self):
        self.position[0] = random.randrange(10, 710)
        self.position[1] = random.randrange(30, 460)
        
class Item(Thing):
    def __init__(self, picture, pos, name):
        Thing.__init__(self, picture, pos)
        self.name = name

    def get_name(self):
        return self.name


class Player(Thing):
    def __init__(self, picture, pos, health=10, defence=1, damage=5):
        Thing.__init__(self, picture, pos)
        self.health = health
        self.defence = defence
        self.damage = damage
        self.items = []

    def move(self, direction, distance):
        if direction == "UP":
            self.position[1] -= distance
        elif direction == "DOWN":
            self.position[1] += distance
        elif direction == "RIGHT":
            self.position[0] += distance
        elif direction == "LEFT":
            self.position[0] -= distance


player = Player("other/2.png", [360, 240])

enemies = []
Yenemies = []
for e in range(10):
    enemy = Thing("other/1.png", [0, 0])
    enemy.move_random()
    enemies.append(enemy)

for i in range(3):
    Yenemy = Thing("other/3.png", [0, 0])
    Yenemy.move_random()
    Yenemies.append(Yenemy)
    
items = []
items.append(Item("boxes/1.png", [random.randrange(10, 710), random.randrange(30, 460)], "helmet"))
items.append(Item("boxes/2.png", [random.randrange(10, 710), random.randrange(30, 460)], "chestplate"))
items.append(Item("boxes/3.png", [random.randrange(10, 710), random.randrange(30, 460)], "necklace"))
items.append(Item("boxes/4.png", [random.randrange(10, 710), random.randrange(30, 460)], "leggings"))
items.append(Item("boxes/5.png", [random.randrange(10, 710), random.randrange(30, 460)], "watch"))


while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
        if event.type == KEYDOWN:
            if event.key == K_w:
                keys["w"] = True
            if event.key == K_a:
                keys["a"] = True
            if event.key == K_s:
                keys["s"] = True
            if event.key == K_d:
                keys["d"] = True
            if event.key == K_SPACE:
                keys[" "] = True
            if event.key == K_q:
                keys["q"] = True
                
        if event.type == KEYUP:
            if event.key == K_w:
                keys["w"] = False
            if event.key == K_a:
                keys["a"] = False
            if event.key == K_s:
                keys["s"] = False
            if event.key == K_d:
                keys["d"] = False
            if event.key == K_SPACE:
                keys[" "] = False
            if event.key == K_q:
                keys["q"] = False
        elif event.type == pygame.USEREVENT + 1:
            seconds += 1

        for Yenemy in Yenemies:     #Have no idea how to simply do it better
            if Yenemy.position[0] <= player.position[0]:
                Yenemy.position[0] += Yspeed
            if Yenemy.position[0] >= player.position[0]:
                Yenemy.position[0] -= Yspeed
            if Yenemy.position[1] <= player.position[1]:
                Yenemy.position[1] += Yspeed
            if Yenemy.position[1] >= player.position[1]:
                Yenemy.position[1] -= Yspeed

        for enemy in enemies:
            if enemy.position[0] <= player.position[0]:
                enemy.position[0] += speed
            if enemy.position[0] >= player.position[0]:
                enemy.position[0] -= speed
            if enemy.position[1] <= player.position[1]:
                enemy.position[1] += speed
            if enemy.position[1] >= player.position[1]:
                enemy.position[1] -= speed
            
    #Consistent movement
    if keys["w"]:
        player.move("UP", speed)
    if keys["a"]:
        player.move("LEFT", speed)
    if keys["s"]:
        player.move("DOWN", speed)
    if keys["d"]:
        player.move("RIGHT", speed)
    if keys["q"]:
       done = True 
    #if keys[" "]:
        #Shoot

    #Walls - Player
    if player.position[1] <= 2:
        player.position[1] += speed
    if player.position[1] >= 433:
        player.position[1] -= speed
    if player.position[0] <= -2:
        player.position[0] += speed
    if player.position[0] >= 690:
        player.position[0] -= speed
        
    for enemy in enemies:
        if enemy.position[1] <= -2:
            enemy.position[1] += 2
        if enemy.position[1] >= 433:
            enemy.position[1] -= 2
        if enemy.position[0] <= -2:
            enemy.position[0] += 2
        if enemy.position[0] >= 690:
            enemy.position[0] -= 2


    for enemy in enemies:
        if player.iscolliding(enemy):
                player.health -= player.damage

    for Yenemy in Yenemies:
        if player.iscolliding(Yenemy):
            player.health -= 50
            
    for item in items:
        if player.iscolliding(item):
            name = item.get_name()
            if name == "helmet":
                #print("helmet picked-up")
                player.items.append("helmet")
                player.defence += 25
                helmets += 1
            if name == "chestplate":
                #print("chestplate picked-up")
                player.defence += 50
                chestplates += 1
            if name == "necklace":
                #print("necklace picked-up")
                player.health += 20
                necklaces += 1
            if name == "leggings":
                #print("leggings picked-up")
                player.defence += 35
                speed += 0.25
                leggings += 1
            if name == "watch":
                #print("watch picked-up")
                watches += 1
                player.items.append("watch")
            item.move_random()

    if player.health <= 0:
        print("Game Over!")
        done = True
    #Text
    Health = myfont.render("Health: " + str(player.health), 50, (255, 255, 255))
    Defence = myfont.render("Defence: " + str(player.defence), 50, (255, 255, 255))    
    Helmet = myfont.render("Helmets: " + str(helmets), 50, (255, 255, 255))
    Chestplate = myfont.render("Chestplates: " + str(chestplates), 50, (255, 255, 255))
    Necklace = myfont.render("Necklaces: " + str(necklaces), 50, (255, 255, 255))
    Leggings = myfont.render("Leggings: " + str(leggings), 50, (255, 255, 255))
    Watch = myfont.render("Watches: " + str(watches), 50, (255, 255, 255))
    if player.items.count("watch") > 0:
        time = myfont.render(str(seconds) + "s", 50, (255, 255, 255))

    #Rendering
    screen.fill(black)
    player.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)

    for Yenemy in Yenemies:
        Yenemy.draw(screen)
        
    for item in items:
        item.draw(screen)
        
    screen.blit(Health, (5, 5))
    screen.blit(Defence, (5, 25))
    screen.blit(Helmet, (5, 60))
    screen.blit(Chestplate, (5, 80))
    screen.blit(Necklace, (5, 100))
    screen.blit(Leggings, (5, 120))
    screen.blit(Watch, (5, 140))
    if player.items.count("watch") > 0:
        screen.blit(time, (10, 460))
    pygame.display.flip()
pygame.quit()
