import pygame, sys, os
from settings import *
from gui import MainMenu


class Game():
    def __init__(self):
        
    #----------------------- general setup ----------------------------#

        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Ray Casting Renderer')
        icon = pygame.image.load(os.path.join('assets', 'icon_radar.png')).convert_alpha()
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()


    #----------------------- instantiate game state--------------------#

        self.menu = MainMenu(self.clock, COLS)
    
    #---------------------- game loop ---------------------------------#

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(1)
            
            self.menu.run()

if __name__== '__main__': 
    game = Game()
    game.run()