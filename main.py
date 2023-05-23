# Inicializar Pygame
import pygame
from agents import *
from pygameClasses import FPS
from quadtree import *

# Dimensiones de la ventana
WIDTH = 1500
HEIGHT = 800

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
fps = FPS()

# Crear el Quadtree con las dimensiones de la ventana
space = Quadtree(0, 0, WIDTH, HEIGHT)

# Crear agentes
num_queens = 1
queens = [Queen(WIDTH, HEIGHT) for _ in range(num_queens)]
for i in queens:
    space.insert_agent(i)
iteration = 0


# Bucle principal del juego
while True:
    iteration += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Verificar si se ha hecho clic izquierdo
                mouse_pos = pygame.mouse.get_pos()
                new_resource = Resource(mouse_pos[0], mouse_pos[1])
                space.insert_agent(new_resource)

    screen.fill((0, 0, 0))


    agents = space.get_all_agents()


    for agent in agents:

    # Actualizar y dibujar a las reinas
        if isinstance(agent, Queen):
            agent.draw(screen)
            if agent.resources >= 10:
                new_recolector = agent.create_recolector()
                agent.resources -= 10
                space.insert_agent(new_recolector)
            

        # Actualizar y dibujar a los recursos
        elif isinstance(agent, Resource):
            if agent.amount <= 0:
                space.remove_agent(agent)
            else:
                agent.draw(screen)

        # Actualizar y dibujar a los recolectores
        elif isinstance(agent, Recolector):

            # verificar si el recolector esta colisionando con algo
            # tener en cuenta q no existen colisiones entre recolectores
            colisiones = space.get_adjacents(agent.x, agent.y, distancia=7)
            if iteration > 100:
                recolectors_in_range_shout = space.get_adjacents(agent.x, agent.y, distancia=50, onlyRecolectors=True)
                agent.shout(recolectors_in_range_shout) # arreglar
            print(agent.resource_counter)
            for colision in colisiones:
                # verificar si el agente esta sobre un recurso y no esta cargado
                if isinstance(colision, Resource):
                    if agent.full == False:
                        agent.full = True
                        agent.resource_counter = 0
                        agent.heading_base = True
                        colision.amount -= 10
                # verificar si esta sobre la base y tiene recursos
                elif isinstance(colision, Queen):
                    if agent.full == True:
                        agent.full = False
                        agent.base_counter = 0
                        agent.heading_base = False
                        colision.resources += 10

            agent.update()
            agent.draw(screen)

    fps.render(screen)
    pygame.display.update()
    fps.clock.tick(60)



