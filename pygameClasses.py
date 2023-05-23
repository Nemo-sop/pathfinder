import pygame


class FPS:
    def __init__(self) -> None:
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Verdana', 20)
        self.text = self.font.render(str(self.clock.get_fps()), True, (255,0,0))
    
    def render(self, display):
        self.text = self.font.render(str(round(self.clock.get_fps(),2)), True, (255,0,0))
        display.blit(self.text, (25, 0))