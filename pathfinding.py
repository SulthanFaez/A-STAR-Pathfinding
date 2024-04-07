#some lines may appear very spaced away because most of the commented lines are deleted

import pygame
import random
import sys
from pygame.locals import *
width,height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pathfinding')
size = 20
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
        self.f = 9999
        self.g = g
        self.h = h
        self.distance = 0
            
    def value(self, start, end):

        ex = self.x - end.x
        ey = self.y - end.y
        #self.distance = 0
        if self.block:
            return 9999
        else:
            manhattan = abs(ex) + abs(ey)
            euclid = ((ex**2)+(ey**2))**0.5
            octile = (max(abs(ex), abs(ey)) + (2**0.5 -1 )*min(abs(ex), abs(ey)))
            chebyshev = max(abs(ex),abs(ey))
            h_cost = manhattan*10 #(max(abs(ex), abs(ey)) + (2**0.5 -1 )*min(abs(ex), abs(ey)))*10
            g_cost = self.distance #max(abs(sx), abs(sy)) + (2**0.5 -1 )*min(abs(sx), abs(sy))
            f_cost = g_cost + h_cost
            self.g = g_cost
            self.h = h_cost
            self.f = f_cost
            #self.distance = 1
            return f_cost
        
    def neighbours(self):
        return [self.id-1, self.id+1, self.id-height//size, self.id+height//size] # self.id+(height//size+1), self.id-(height//size+1), self.id+(height//size-1), self.id-(height//size-1)]

nodes = {"id":[], "value":[], "value_unchecked":[], "parent":[]}
def generate():
    generate_ids = False
    if nodes["id"] == []:
        generate_ids = True
    for i in range(width//size):
        for j in range(height//size):
            if generate_ids:
                nodes["id"].append(Node(j, i, (i*height//size)+j, 0, 0))
        
            if random.randint(0, 100) < 35:
                nodes["id"][(i*height//size)+j].block = True
                nodes["id"][(i*height//size)+j].colour = (0,0,0)

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
        node_indices = find_indices(nodes["value_unchecked"], min_f_cost)
        node_scores = [(nodes["id"][i].f, nodes["id"][i].g) for i in node_indices]
        min_node_score = min(node_scores)
        node_index = node_indices[node_scores.index(min_node_score)]
        node = [node_index]

    for n in node:

        nodes["value_unchecked"][n] = 9999    
      
        for _ in nodes["id"][n].neighbours():

            if _ >=0 and _ < len(nodes["id"]):
                
                if nodes["id"][_].checked == True:
                    nodes["value_unchecked"][_] = 9999 
                
                # if nodes["id"][_].value(nodes["id"][s], nodes["id"][e]) < 1000 and nodes["id"][_].start == False and nodes["id"][_].end == False:
                #     if  nodes["id"][_].colour != (255, 0,0):
                #         nodes["id"][_].colour = (255, 165, 0)    
                        
                sx = nodes["id"][n].x - nodes["id"][_].x
                sy = nodes["id"][n].y - nodes["id"][_].y
                if n != s:
                    if abs(n - _) == height//size+1 or abs(n - _) == (height//size-1):
                        nodes["id"][_].distance = nodes["id"][n].distance + 14
 
                    else:
                        nodes["id"][_].distance = (nodes["id"][n].distance + 10)       

                if nodes["id"][_].checked == False:
                    if nodes["id"][_].value(nodes["id"][s], nodes["id"][e]) < nodes["value_unchecked"][_]:
                        nodes["value"][_] = nodes["id"][_].value(nodes["id"][s], nodes["id"][e])
                        nodes["value_unchecked"][_] = nodes["id"][_].value(nodes["id"][s], nodes["id"][e])                        
                    nodes["id"][_].parent = nodes["id"][n].id
                    nodes["parent"][_] = nodes["id"][n].id
                    
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
found = False
node_count = 0

while running:
    mouse = pygame.mouse.get_pressed()
    screen.fill((0,0,0))
    for _ in nodes["id"]:
        pygame.draw.rect(screen, _.colour, pygame.Rect(_.x * size, _.y * size, size-1, size-1))
        # screen.blit(font.render(str(_.g), True, (0,0,0)), (_.x*size, _.y*size))
    
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False
            break
        hitbox = 3
        if mouse[0]:
            mx,my = pygame.mouse.get_pos()

            for node in nodes["id"]:

                if node.x*size-hitbox <= mx <= node.x*size + size+hitbox and node.y*size-hitbox <= my <= node.y*size + size+hitbox:
                    node.colour = (0, 0, 0)
                    node.block = True
                    
        
        if mouse[2]:
            mx,my = pygame.mouse.get_pos()
            for node in nodes["id"]:

                if node.x*size-hitbox <= mx <= node.x*size + size+hitbox and node.y*size-hitbox <= my <= node.y*size + size+hitbox:
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
                    found = False
            if event.key == pygame.K_r:
                path = False
                found = False
                s, e = -100, -100
                nodes = {"id":[], "value":[], "value_unchecked":[], "parent":[]}
                generate()
                it = 0


    if path == True:
        arr = []
        expansion= [] 
        node_count = 0
        while found != True:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running= False
                        found = True
                        break
            j = 0
            pathfinding(it,nodes,s,e)
            for i in nodes["id"]:
                if i.checked == True:
                    j += 1
            
            expansion.append(j)
            #print(expansion)
            node_count += 1
            if node_count >= len(nodes["id"]) - sum([i.block for i in nodes["id"]]):
                path = False
                found = True
                break                    
            if it > 0:
                if expansion[-1] <= expansion[0]:
                    path = False
                    found = True
                    print('No Path')
                    break 

                expansion.pop(0)
            
            for node in nodes["id"]:
                
                if nodes["id"][node.id].checked == True:
                    
                    for n in node.neighbours():

                        if n > 0 and n < (width//size * height//size):
                            

                            if n == e:
                                
                                path = False
                                found = True
                                for i in range(len(nodes["parent"])):

                                    nodes["parent"][i] = nodes["id"][i].parent
                                print(len(shortest(nodes, node.id, s)))
                                for _ in shortest(nodes, node.id, s):
                                    #try nodes["id"][_].colour:
                                    
                                    if _ < len(nodes["id"]):
                                        found = True
                                        nodes["id"][_].colour = (74, 171, 255)
                                        
                                    else:
                                        print("No Path")

            

            # for _ in nodes["id"]:
            #     pygame.draw.rect(screen, _.colour, pygame.Rect(_.x * size, _.y * size, size-1, size-1))
            #     screen.blit(font.render(str(_.f), True, (0,0,0)), (_.x*size, _.y*size))
    
            pygame.display.flip()




                

            it+=1
        
            
        #print(it, "B")
    it = 0
    
    pygame.time.Clock().tick(10000000)


    
