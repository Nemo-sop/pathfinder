import pygame
import math
import random

class tester():
    def __init__(self):
        self.speed = random.randint(1, 1)
        self.angle = random.uniform(0, 2 * math.pi)
        self.x = 0
        self.y = 0

    def cambiar_direccion_hacia_punto(self, objetivo_x, objetivo_y):
        dx = objetivo_x - self.x
        dy = objetivo_y - self.y
        angulo_radianes = math.atan2(dy, dx)
        angulo_grados = math.degrees(angulo_radianes)
        self.angle = angulo_grados

        pos1 = (self.x, self.y)
        pos2 = (objetivo_x, objetivo_y)
        #pygame.draw.line(screen,(255,255,255), pos1, pos2)
        #pygame.draw.circle(screen,(255,255,255), (self.x-3, self.y-3), 2)

    def rotate_180_degrees(self):
        self.angle += 180

test = tester()

print('angulo inicial: ', test.angle)
test.rotate_180_degrees()
print('angulo dsp del giro de 180 grados: ', test.angle)
test.cambiar_direccion_hacia_punto(1, 1)
print('angulo esperado, 45, angulo obtenido: ', test.angle)

