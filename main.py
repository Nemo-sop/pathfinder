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
pygame.display.set_caption("Window 1")
fps = FPS()

# Crear el Quadtree con las dimensiones de la ventana
space = Quadtree(0, 0, WIDTH, HEIGHT)

# Crear agentes
num_queens = 1
queens = [Queen(WIDTH, HEIGHT) for _ in range(num_queens)]
for i in queens:
    space.insert_agent(i)



# Bucle principal del juego
while True:

    count = {'Reinas': 0,
         'Recolectores': 0,
         'Recursos': 0,
         'Feromonas': 0}
    
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

        # Actualizar y dibujar a los recursos
        if isinstance(agent, Resource):
            count['Recursos'] += 1
            if agent.amount <= 0:
                space.remove_agent(agent)
            else:
                agent.draw(screen)

            recolectors_in_resource = space.get_adjacents(agent.x, agent.y, distancia=20 ,onlyRecolectors=True)

            for recolector in recolectors_in_resource:
                recolector.heading = 'home'


        # Actualizar y dibujar a los recolectores
        elif isinstance(agent, Recolector):
            count['Recolectores'] += 1
            agent.update()
            new_pheromone = agent.leave_phermone()
            if new_pheromone:
                space.insert_agent(new_pheromone)

            close_pheromones = space.get_adjacents(agent.x, agent.y, onlyPheromones=True)
            close_home_pheromones = [pheromone for pheromone in close_pheromones if pheromone.type == 'home']
            close_resource_pheromones = [pheromone for pheromone in close_pheromones if pheromone.type == 'resource']
            '''
            if agent.heading == 'home':
                agent.update_direction(close_home_pheromones)
            else:
                agent.update_direction(close_resource_pheromones) 
            '''
            agent.draw(screen)


        
        # Actualizar y dibujar la feromonas
        elif isinstance(agent, Pheromone):
            count['Feromonas'] +=1
                
            agent.update()
            if agent.strength <= 0:
                space.remove_agent(agent)
                count['Feromonas'] -= 1
            agent.draw(screen)


        
        # Actualizar y dibujar a las reinas
        elif isinstance(agent, Queen):
            count['Reinas'] += 1
            agent.draw(screen)
            if agent.resources >= 10:
                new_recolector = agent.create_recolector()
                agent.resources -= 10
                space.insert_agent(new_recolector)
        
    font = pygame.font.SysFont('Verdana', 20)
    text = font.render(str("Agent Count: "+str(len(agents))), True, (255,0,0))
    screen.blit(text, (25, 50))

    pygame.draw.line(screen,(255,255,255), (10, 10), (10, 60))

    fps.renderFPS(screen)
    pygame.display.update()
    fps.clock.tick(35)
    print(count)

    



