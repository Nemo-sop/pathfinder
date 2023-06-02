import math
import random
from typing import Any

import numpy as np
import pygame


class Recolector():

    def __instancecheck__(self, __instance: Any) -> bool:
        return isinstance(__instance, Recolector)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.speed = random.randint(5, 8)
        self.angle = random.uniform(0, 360)
        self.color = (255, 255, 255)
        self.heading = 'resource'
        self.distance_traveled_for_pheromone = 10
        
    def update(self):
        # Actualizar la posicion
        self.x += (self.speed * math.cos(self.angle))
        self.y += (self.speed * math.sin(self.angle))

        self.pos = (round(self.x), round(self.y))

        # Rebotar en los bordes de la ventana
        if self.x < 0 or self.x > 1500:
            self.angle = math.pi - self.angle
        if self.y < 0 or self.y > 800:
            self.angle = -self.angle

        self.distance_traveled_for_pheromone += 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)
        
    def leave_phermone(self):
        if self.heading == 'resource':
            type = 'home'
        else:
            type = 'resource'

        if self.distance_traveled_for_pheromone >= self.speed *1.3:
            self.distance_traveled_for_pheromone = 0
            return Pheromone(self.x, self.y, type)
        
    def grab_resource(self):
        self.heading = 'home'
        
    def update_direction(self, pheromones):
        if len(pheromones) == 0:
            return

        sum_vector = (0, 0)

        for pheromone in pheromones:
            pheromone_vector = (
                pheromone.x - self.x,
                pheromone.y - self.y
            )
            sum_vector = (
                sum_vector[0] + pheromone_vector[0],
                sum_vector[1] + pheromone_vector[1]
            )

        magnitude = math.sqrt(sum_vector[0]**2 + sum_vector[1]**2)
        if magnitude > 0:
            normalized_vector = (
                sum_vector[0] / magnitude,
                sum_vector[1] / magnitude
            )
            self.angle = math.atan2(normalized_vector[1], normalized_vector[0])
        else:
            self.angle = self.angle

        self.angle = math.degrees(self.angle)

class Pheromone():
    def __init__(self, x, y, type) -> None:
        self.strength = 50
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)
        self.type = type
        if type == 'resource':
            self.color = (0, 0, 255)
        if type == 'home':
            self.color = (255, 0, 0)

    def update(self):
        self.strength -= 1

    def draw(self, screen):
        intensity = self.strength / 100
        color = (
            max(0, min(int(self.color[0] * intensity), 255)),
            max(0, min(int(self.color[1] * intensity), 255)),
            max(0, min(int(self.color[2] * intensity), 255))
        )
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 1)
    


class Queen():

    def __instancecheck__(self, __instance: Any) -> bool:
        return isinstance(__instance, Queen)
    
    def __init__(self, WIDTH, HEIGHT) -> None:
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.resources = 100
        self.color = (255, 255, 0)
        self.pos = (self.x, self.y)
        

    def create_recolector(self):
        return Recolector(self.x, self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)
    

class Resource():

    def __instancecheck__(self, __instance: Any) -> bool:
        return isinstance(__instance, Resource)   
    
    def __init__(self, x, y) -> None:
        self.amount = 10000000
        self.color = (0, 255, 0)
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)#self.amount/100)

    def update():
        pass
