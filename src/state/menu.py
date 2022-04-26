import pygame
import pygame_menu

class MenuState:

    def __init__(self, screen_resolusion) -> None:
        self.screen_resolution = screen_resolusion
        self.menu = pygame_menu.Menu(
            width=screen_resolusion[0],
            height=screen_resolusion[1],
            theme=pygame_menu.themes.THEME_BLUE,
            title='Welcome',
        )
        self.menu.add.label('Resize the window!')
        self.menu.add.selector('Difficulty: ', [('Hard', 1), ('Easy', 2)])
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.menu.enable()

    def update(self, *args, **kwargs):
        events = pygame.event.get()
        screen = kwargs['screen']
        screen.fill((0, 0, 0))
        self.menu.update(events)
        self.menu.draw(screen)
        pygame.display.flip()
