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
        
        self.full = False

        self.base_counter = 0
        self.resource_counter = 2000

        self.heading_base = False

        self.speed = random.randint(5, 15)
        self.angle = random.uniform(0, 2 * math.pi)

        self.color = (0, 255, 0)
        

    def update(self):
        # Actualizar la posicion
        self.x += (self.speed * math.cos(self.angle))
        self.y += (self.speed * math.sin(self.angle))
        

        self.pos = (round(self.x), round(self.y))

        # Actualizar indice de confianza
        self.base_counter += 1
        self.resource_counter += 1

        # Rebotar en los bordes de la ventana
        if self.x < 0 or self.x > 1500:
            self.angle = math.pi - self.angle
        if self.y < 0 or self.y > 800:
            self.angle = -self.angle

    def draw(self, screen):
        if self.full:
            self.color = (255, 0, 0)
        else:
            self.color = (0, 255, 0)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)

    def shout(self, recolectores):
        pass
    """ implementacion vieja donde un recolector actualizaba a sus vecinos
        for recolector in recolectores:
            if recolector.base_counter > self.base_counter:
                recolector.base_counter = self.base_counter+50
                if recolector.heading_base:
                    recolector.cambiar_direccion_hacia_punto(self.x, self.y)
            else:
                self.base_counter = recolector.base_counter+50
                if self.heading_base:
                    recolector.cambiar_direccion_hacia_punto(recolector.x, recolector.y)

            if recolector.resource_counter > self.resource_counter:
                recolector.resource_counter = self.resource_counter+50
                if not recolector.heading_base:
                    recolector.cambiar_direccion_hacia_punto(self.x, self.y)
            else:
                self.resource_counter = recolector.resource_counter+50
                if not self.heading_base:
                    recolector.cambiar_direccion_hacia_punto(recolector.x, recolector.y)
            """
    
    def hear(self, recolectores_cercanos):
        for recolector in recolectores_cercanos:
            # si el recolector esta mas cerca de la base, actualizo mi contador
            if recolector.base_counter < self.base_counter:
                self.base_counter = recolector.base_counter+50
                # si yo me estoy dirigiendo a la base, cambio mi direccion hacia el
                if self.heading_base:
                    self.cambiar_direccion_hacia_punto(recolector.x, recolector.y)

            # si el recolector esta mas cerca del recurso, actualizo mi contador
            if recolector.resource_counter < self.resource_counter:
                self.resource_counter = recolector.resource_counter+50
                # si yo me estoy dirigiendo al recurso, cambio mi direccion hacia el
                if not recolector.heading_base:
                    self.cambiar_direccion_hacia_punto(recolector.x, recolector.y)
            

    def cambiar_direccion_hacia_punto(self, objetivo_x, objetivo_y):
        dx = objetivo_x - self.x
        dy = objetivo_y - self.y
        angulo_radianes = math.atan2(dy, dx)
        #print(self.angle)
        self.angle = angulo_radianes
        #print(self.angle)

    def rotate_180_degrees(self):
        self.angle += math.pi


class Queen():

    def __instancecheck__(self, __instance: Any) -> bool:
        return isinstance(__instance, Queen)
    
    def __init__(self, WIDTH, HEIGHT) -> None:
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.resources = 1000
        self.color = (255, 255, 0)
        self.pos = (self.x, self.y)
        self.heading_base = False

    def create_recolector(self):
        return Recolector(self.x, self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 10)

    def shout(self, recolectores, colision):
        pass 
    # Esto lo tuve que agregar pq por alguna razon el quadtree no le funciona la opcion
    # onlyRecolectors en el metodo de get_adjacent
    # Sin embargo queda abierta a la posibilidad que la reina se comunique con algun fin
    # con los recolectores, ya sea para avisar de su posicion o enviar ordenes mas complejas
    # ARREGLADO 

class Resource():

    def __instancecheck__(self, __instance: Any) -> bool:
        return isinstance(__instance, Resource)   
    
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
