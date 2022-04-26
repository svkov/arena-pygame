import pygame
from src.game import Game


def main():
    pygame.init()
    pygame.display.set_caption("Arena")
    pygame.font.init()
    game = Game()
    while game.running:
        game.update()


if __name__ == "__main__":
    main()
