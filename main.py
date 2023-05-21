# Inicializar Pygame
import pygame
from agents import *

# Dimensiones de la ventana
WIDTH = 1600
HEIGHT = 1000

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Crear agentes
num_queens = 1
queens = [Queen(WIDTH, HEIGHT) for _ in range(num_queens)]
agents = []
resources = []


# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Verificar si se ha hecho clic izquierdo
                mouse_pos = pygame.mouse.get_pos()
                new_resource = Resource(mouse_pos[0], mouse_pos[1])
                resources.append(new_resource)

    screen.fill((0, 0, 0))

    # Actualizar y dibujar a las reinas
    for queen in queens:
        queen.draw(screen)
        if queen.resources >= 10:
            new_recolector = queen.create_recolector()
            queen.resources -= 10
            agents.append(new_recolector)
        

    # Actualizar y dibujar a los recursos
    for resource in resources:
        if resource.amount <= 0:
            resources.remove(resource)
        else:
            resource.draw(screen)

    # Actualizar y dibujar a los agentes
    for agente in agents:

        # verificar si el agente esta sobre un recurso
        for resource in resources:
            if agente.pos in obtener_coordenadas_en_radio(resource.pos):
                agente.shout(agents)
                if agente.full == False:
                    agente.full = True
                    agente.resource_counter = 0
                    agente.heading_base = True
                    resource.amount -= 10

        # verificar si esta sobre la base y tiene recursos
        for queen in queens:
            if agente.pos == obtener_coordenadas_en_radio(queen.pos):
                agente.shout(agents)
                if agente.full == True:
                    agente.full = False
                    agente.base_counter = 0
                    agente.heading_base = False
                    queen.resources += 10

        agente.update()
        agente.draw(screen)


    pygame.display.flip()
    clock.tick(60)