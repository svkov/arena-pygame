import pygame
import pygame_menu

class MenuState:

    def __init__(self, game, screen_resolusion) -> None:
        self.game = game
        self.screen_resolution = screen_resolusion
        self.menu = pygame_menu.Menu(
            width=screen_resolusion[0],
            height=screen_resolusion[1],
            theme=pygame_menu.themes.THEME_DEFAULT,
            title='Arena',
        )
        self.menu.add.button('Start game', self.start_game)
        self.menu.add.selector('Difficulty: ', [('Hard', 1), ('Easy', 2)])
        self.menu.add.button('Settings', self.to_settings)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)
        self.current_menu = self.menu
        self.current_menu.enable()

        self.settings_menu = pygame_menu.Menu(
            width=screen_resolusion[0],
            height=screen_resolusion[1],
            theme=pygame_menu.themes.THEME_DEFAULT,
            title='Settings'
        )
        self.fps = self.game.fps
        self.fps_selectable = [('30', 30), ('60', 60), ('90', 90)]
        self.fps_index = self.select_fps_index()

        self.resolution_selectable = [
            ('800x600', (800, 600)),
            ('1280x720', (1280, 720)),
            ('1920x1080', (1920, 1080)),
            ('2560x1080', (2560, 1080))
        ]
        self.resolution_index = self.select_resolution_index()

        self.settings_menu.add.selector('FPS: ', self.fps_selectable,
                                        default=self.fps_index, onchange=self.on_fps_change)
        self.settings_menu.add.selector('Resolution: ', self.resolution_selectable,
                                        default=self.resolution_index, onchange=self.on_resolution_change)
        self.settings_menu.add.button('Back', self.to_main)

    def select_fps_index(self):
        for index, (str_fps, fps) in enumerate(self.fps_selectable):
            if fps == self.fps:
                return index

    def select_resolution_index(self):
        for index, (str_fps, resolution) in enumerate(self.resolution_selectable):
            if resolution == self.screen_resolution:
                return index

    def update(self, *args, **kwargs):
        events = pygame.event.get()
        screen = kwargs['screen']
        screen.fill((0, 0, 0))
        self.current_menu.update(events)
        self.current_menu.draw(screen)

    def start_game(self):
        self.game.start_game()

    def on_fps_change(self, selected, *args, **kwargs):
        print(selected)

    def on_resolution_change(self, selected, *args, **kwargs):
        print(selected)

    def to_settings(self):
        self.current_menu.disable()
        self.current_menu = self.settings_menu
        self.current_menu.enable()

    def to_main(self):
        self.current_menu.disable()
        self.current_menu = self.menu
        self.current_menu.enable()
