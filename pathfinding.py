#some lines may appear very spaced away because most of the commented lines are deleted

import pygame
import random
import sys
from pygame.locals import *
width,height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pathfinding')
size = 15
pygame.init()
font = pygame.font.SysFont('Arial', size-10)
class Node:
    def __init__(self, x, y, id, g, h):
        self.x = x
        self.y = y
        self.id = id
        self.start = False
        self.end = False
        self.block = False
        self.colour = (255, 255, 255)
        self.checked = False
        self.parent = 9999
        self.f = 0
        self.g = g
        self.h = h
        


        

    def value(self, start, end):
        if self.block == True:
            return 9999
        else:

            if abs(self.parent - self.id) ==self.id+(height//size+1) or abs(self.parent - self.id) == self.id+(height//size-1):
                return ((self.x-start.x)**2 + (self.y-start.y)**2)**0.5 + ((self.x-end.x)**2+(self.y-end.y)**2)**0.5 + 2
            else: 
                sx =(start.x - self.x)#**2
                sy =(start.y - self.y)#**2
                ex =(self.x-end.x)#**2
                ey = (self.y-end.y)


                manhattan = (abs(ex) + abs(ey))
                
                custom = (abs(sx)+abs(sy))
                octile = max(abs(ex), abs(ey)) + (2**0.5 - 1)*min(abs(ex), abs(ey))
                chebyshev = max(abs(ex), abs(ey))
                euclid = (ex**2+ey**2)**0.5

                gCost = max(abs(sx), abs(sy)) + (2**0.5 - 1)*min(abs(sx), abs(sy))
                hCost = manhattan
                self.g = gCost
                self.h = hCost
                
                fCost = gCost + hCost
                self.f = fCost

                
                return  fCost 
    def neighbours(self):
        return [self.id-1, self.id+1, self.id-height//size, self.id+height//size] #self.id+(height//size+1), self.id-(height//size+1), self.id+(height//size-1), self.id-(height//size-1)]

nodes = {"id":[], "value":[], "value_unchecked":[], "parent":[]}
def generate():
    
    for i in range(width//size):
        for j in range(height//size):
            nodes["id"].append(Node(j, i, (i*height//size)+j, 0, 0))
        



            nodes["value"].append(9999)
            nodes["value_unchecked"].append(9999)
            nodes["parent"].append(9999)

    for i in nodes["id"]:
        
        if i.id % (width//size) == 0 or (i.id % (width//size)  ==  width//size - 1):
            i.block = True
            i.colour = (0, 0,0)    
    for i in nodes["id"][:width//size]:
        i.block = True
        i.colour = (0, 0,0)    
    for i in nodes["id"][-width//size:]:
        i.block = True
        i.colour = (0,0,0)

def find_indices(arr, target):
    indices = []
    for i in range(len(arr)):
        if arr[i] == target:
            indices.append(i)
    return indices

it = 0


s,e=-100,-100
running = True

def pathfinding(it, nodes, s, e):
    if it == 0:
        node = [s]
    else:
        min_f_cost = min(nodes["value_unchecked"])  
        node_indices = [i for i, f_cost in enumerate(nodes["value_unchecked"]) if f_cost == min_f_cost] 
        node_index = min(node_indices, key=lambda idx: nodes["id"][idx].g)  

        node = [node_index]

    for n in node:

        nodes["value_unchecked"][n] = 9999    
        d = [(nodes["value_unchecked"][n] , node)]

        
        for _ in nodes["id"][n].neighbours():

            if _ >=0 and _ < len(nodes["id"]):
                if nodes["id"][_].value(nodes["id"][s], nodes["id"][e]) < 1000 and nodes["id"][_].start == False and nodes["id"][_].end == False:
                    if  nodes["id"][_].colour != (255, 0,0):
                        nodes["id"][_].colour = (255, 165, 0)    
                if (nodes["id"][_].colour != (74, 171, 255)):
                    if nodes["id"][_].checked == False:
                        nodes["value"][_] = nodes["id"][_].value(nodes["id"][s], nodes["id"][e])
                        nodes["value_unchecked"][_] = nodes["id"][_].value(nodes["id"][s], nodes["id"][e])
                        d.append(nodes["value_unchecked"][_])






                        nodes["id"][_].parent = nodes["id"][n].id



                    if nodes["id"][_].checked == True:
                        nodes["value_unchecked"][_] = 9999 
            







            nodes["id"][n].checked = True








        if nodes["id"][n].colour != (74, 171, 255):
           nodes["id"][n].colour = (255, 0, 0)









                    

        
def shortest(nodes, i, s):
    m = []
    _ = i
    r = True
    for f in range(400):
        
        if _ != s:
            m.append(_)

        else:
            break
        if _ < len(nodes["id"]):
            _ = nodes["parent"][_]
    return m
            
        


path = False
generate()

while running:
    mouse = pygame.mouse.get_pressed()
    screen.fill((0,0,0))
    for _ in nodes["id"]:
        pygame.draw.rect(screen, _.colour, pygame.Rect(_.x * size, _.y * size, size-1, size-1))
        screen.blit(font.render(str(_.f), True, (0,0,0)), (_.x*size, _.y*size))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False
            break
        if mouse[0]:
            mx,my = pygame.mouse.get_pos()

            for node in nodes["id"]:

                if node.x*size <= mx <= node.x*size + size and node.y*size <= my <= node.y*size + size:
                    node.colour = (0, 0, 0)
                    node.block = True
                    
                    
        if mouse[2]:
            mx,my = pygame.mouse.get_pos()
            for node in nodes["id"]:

                if node.x*size <= mx <= node.x*size + size and node.y*size <= my <= node.y*size + size:
                    node.colour = (255, 255, 255)
                    node.block = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                mx,my = pygame.mouse.get_pos()

                for node in nodes["id"]:

                    if node.x*size <= mx <= node.x*size+ size and node.y*size <= my <= node.y*size + size and s < 0:
                        
                        node.colour = (74, 171, 255)
                        node.start = True
                        s = node.id
            if event.key == pygame.K_e:
                mx,my = pygame.mouse.get_pos()

                for node in nodes["id"]:

                    if node.x*size <= mx <= node.x*size + size and node.y*size <= my <= node.y*size + size and e < 0:
                        
                        node.colour = (74, 171, 255)
                        node.end = True
                        e = node.id                       
            
            if event.key == pygame.K_SPACE:
                if it == 0:
                    path = True
            if event.key == pygame.K_r:
                path = False
                s, e = -100, -100
                nodes = {"id":[], "value":[], "value_unchecked":[], "parent":[]}
                generate()
                it = 0


    if path == True:
        arr = [] 
        
        pathfinding(it,nodes,s,e)
        for node in nodes["id"]:
            
            if nodes["id"][node.id].checked == True:
                
                for n in node.neighbours():

                    if n > 0 and n < (width//size * height//size):
                        

                        if n == e:
                            path = False
                            for i in range(len(nodes["parent"])):

                                nodes["parent"][i] = nodes["id"][i].parent
                                
                            for _ in shortest(nodes, node.id, s):
                                nodes["id"][_].colour = (74, 171, 255)


                

        it+=1


    
