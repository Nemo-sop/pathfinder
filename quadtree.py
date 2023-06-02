import math

from agents import Pheromone, Recolector


class Quadtree:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.agents = []
        self.children = [None, None, None, None]

    def update_quadtree(self):
        # Crear un nuevo Quadtree vacío con las mismas dimensiones
        nuevo_quadtree = Quadtree(self.x, self.y, self.width, self.height)

        # Insertar los agentes actualizados en el nuevo Quadtree
        for agent in self.agents:
            nuevo_quadtree.insertar_agente(agent)

        # Reemplazar el Quadtree anterior con el nuevo Quadtree actualizado
        self.agents = nuevo_quadtree.agents
        self.children = nuevo_quadtree.children

    def insert_agent(self, agent):
        if not self.contains_point(agent.x, agent.y):
            return

        if len(self.agents) < 4:  # Número máximo de agentes por celda del Quadtree
            self.agents.append(agent)
        else:
            if self.children[0] is None:
                self.split()

            for child in self.children:
                child.insert_agent(agent)

    def get_agent(self, x, y):
        if not self.contains_point(x, y):
            return None

        # Podar si no hay agentes en esta celda
        if len(self.agents) == 0:
            return None

        # Buscar agentes en esta celda que coincidan con el punto
        for agent in self.agents:
            if agent.x == x and agent.y == y:
                return agent

        # Podar si no hay hijos o si el punto está completamente contenido en los hijos
        if self.children[0] is None or self.contiene_punto_completo(x, y):
            return None

        # Buscar en los hijos
        for child in self.children:
            agente = child.obtener_agente_en_punto(x, y)
            if agente is not None:
                return agente

        return None
    
    def get_adjacents(self, x, y, distancia=55, onlyRecolectors=False, onlyPheromones=False):
        agentes_en_distancia = []

        for agent in self.agents:
            if self.calc_dist(agent.x, agent.y, x, y) <= distancia:
                if onlyRecolectors:
                    if isinstance(agent, Recolector):
                        agentes_en_distancia.append(agent)
                if onlyPheromones:
                    if isinstance(agent, Pheromone): 
                        agentes_en_distancia.append(agent)
                else: 
                    agentes_en_distancia.append(agent)                 

        if self.children[0] is not None:
            for child in self.children:
                agentes_en_distancia.extend(child.get_adjacents(x, y, distancia, onlyRecolectors, onlyPheromones))
        
        return agentes_en_distancia

    def calc_dist(self, x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


    def contains_point(self, x, y):
        return (
            self.x <= x < self.x + self.width and
            self.y <= y < self.y + self.height
        )

    def split(self):
        half_width = self.width / 2
        half_height = self.height / 2
        x = self.x
        y = self.y

        self.children[0] = Quadtree(x, y, half_width, half_height)
        self.children[1] = Quadtree(x + half_width, y, half_width, half_height)
        self.children[2] = Quadtree(x, y + half_height, half_width, half_height)
        self.children[3] = Quadtree(x + half_width, y + half_height, half_width, half_height)

        for agent in self.agents:
            for child in self.children:
                child.insert_agent(agent)

        self.agents = []

    def get_all_agents(self):
            agentes = []

            if len(self.agents) > 0:
                agentes.extend(self.agents)

            if self.children[0] is not None:
                for child in self.children:
                    agentes.extend(child.get_all_agents())

            return agentes
    
    def remove_agent(self, agent):
        cell = self.get_cell_containing_point(agent.x, agent.y)
        if cell is not None:
            if agent in cell.agents:
                cell.agents.remove(agent)
                return True
        return False
    
    def get_cell_containing_point(self, x, y):
        if not self.contains_point(x, y):
            return None

        if self.children[0] is None:
            return self

        for child in self.children:
            cell = child.get_cell_containing_point(x, y)
            if cell is not None:
                return cell

        return None
