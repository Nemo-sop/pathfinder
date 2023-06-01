import pygame


class FPS:
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Verdana', 20)
        self.text = self.font.render(str(self.clock.get_fps()), True, (255,0,0))
    
    def renderFPS(self, display):
        self.text = self.font.render(str(round(self.clock.get_fps(),2)), True, (255,0,0))
        display.blit(self.text, (25, 0))

    def renderAgentCount(self, display):
        font = pygame.font.SysFont('Verdana', 20)
        text = font.render(str("aca el lem"), True, (255,0,0))
        display.blit(text, (50, 0))