import math
import random

import numpy as np
import pygame


class Recolector():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = random.randint(5,9)
        self.full = False
        self.base_counter = 0
        self.resource_counter = 2600
        self.heading_base = False

        self.speed = random.uniform(1, 10)
        self.angle = random.uniform(0, 2 * math.pi)

        self.color = (0, 255, 0)
        self.pos = (self.x, self.y)

    def update(self):
        # Actualizar la posicion
        self.x += (self.speed * math.cos(self.angle))
        self.y += (self.speed * math.sin(self.angle))
        

        self.pos = (round(self.x), round(self.y))

        # Actualizar contadores
        self.base_counter += 1
        self.resource_counter += 1

        # Rebotar en los bordes de la ventana
        if self.x < 0 or self.x > 1600:
            self.angle = math.pi - self.angle
        if self.y < 0 or self.y > 1000:
            self.angle = -self.angle

    def draw(self, screen):
        if self.full:
            self.color = (255, 0, 0)
        else:
            self.color = (0, 255, 0)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 5)


    def hear(self, agents, distance=50):
        for agent in agents:
            # Verificar si lo puedo escuchar
            if agent.pos in obtener_coordenadas_en_radio(self.pos, distance):
                if agent.base_counter < self.base_counter:
                    self.base_counter = agent.base_counter + 50
                    if self.heading_base == True:
                        self.cambiar_direccion_hacia_punto(agent.x, agent.y)
                if agent.resource_counter < self.resource_counter:
                    self.resource_counter = agent.resource_counter + 50
                    if self.heading_base == False:
                        self.cambiar_direccion_hacia_punto(agent.x, agent.y)
        

    def shout(self, agents, distance=100):
        radius = obtener_coordenadas_en_radio(self.pos, distance)
        for pos in radius:
            for agent in agents:
                if agent.pos in pos:
                    #
                    if self.base_counter < agent.base_counter:
                        agent.base_counter = self.base_counter+distance
                        if agent.heading_base == True:
                            agent.cambiar_direccion_hacia_punto(self.x, self.y) 
                    if self.resource_counter < agent.resource_counter:
                        agent.resource_counter = self.resource_counter+distance
                        if agent.heading_base == False:
                            agent.cambiar_direccion_hacia_punto(self.x, self.y) 

    def cambiar_direccion_hacia_punto(self, objetivo_x, objetivo_y):
        dx = objetivo_x - self.x
        dy = objetivo_y - self.y
        angulo_radianes = math.atan2(dy, dx)
        print(self.angle)
        self.angle = angulo_radianes
        print(self.angle)


class Queen():
    def __init__(self, WIDTH, HEIGHT) -> None:
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.resources = 1000
        self.color = (255, 255, 0)
        self.pos = (self.x, self.y)

    def create_recolector(self):
        return Recolector(self.x, self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)

class Resource():
    def __init__(self, x, y) -> None:
        self.amount = 1000
        self.color = (255, 255, 255)
        self.x = x
        self.y = y
        self.pos = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.amount/100)

    def update():
        pass

def obtener_coordenadas_en_radio(punto_central, radio=8):
    puntos_en_radio = []
    x_central, y_central = punto_central

    for x in range(x_central - radio, x_central + radio + 1):
        for y in range(y_central - radio, y_central + radio + 1):
            distancia = abs(x - x_central) + abs(y - y_central)
            if distancia <= radio:
                puntos_en_radio.append((x, y))

    return puntos_en_radio
