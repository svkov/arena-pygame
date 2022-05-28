import pygame
import pygame_menu

class MenuState:

    def __init__(self, game, screen_resolution) -> None:
        self.game = game
        self.screen_resolution = screen_resolution
        self.init_menu()
        self.init_settings()
        self.init_help()
        self.current_menu = self.menu
        self.current_menu.enable()

    def init_menu(self):
        self.menu = pygame_menu.Menu(
            width=self.screen_resolution[0],
            height=self.screen_resolution[1],
            theme=pygame_menu.themes.THEME_DEFAULT,
            title='Arena',
        )
        self.menu.add.button('Start game', self.start_game)
        self.menu.add.selector('Difficulty: ', [('Hard', 1), ('Easy', 2)])
        self.menu.add.button('Settings', self.to_settings)
        self.menu.add.button('Help', self.to_help)
        self.menu.add.button('Quit', pygame_menu.events.EXIT)

    def init_settings(self):
        self.settings_menu = pygame_menu.Menu(
            width=self.screen_resolution[0],
            height=self.screen_resolution[1],
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
            ('2560x1440', (2560, 1440))
        ]
        self.resolution_index = self.select_resolution_index()

        warning = 'WARNING: changes will apply after restart'
        warning_color = (255, 255, 50)
        self.warning_label = self.settings_menu.add.label(warning, font_color=warning_color)
        self.settings_menu.add.selector('FPS: ', self.fps_selectable,
                                        default=self.fps_index, onchange=self.on_fps_change)
        self.settings_menu.add.selector('Resolution: ', self.resolution_selectable,
                                        default=self.resolution_index, onchange=self.on_resolution_change)
        self.apply_button = self.settings_menu.add.button('Apply', self.apply_changes)
        self.settings_menu.add.button('Back', self.to_main)
        self.warning_label.hide()
        self.apply_button.hide()

    def init_help(self):
        self.help_menu = pygame_menu.Menu(
            width=self.screen_resolution[0],
            height=self.screen_resolution[1],
            theme=pygame_menu.themes.THEME_DEFAULT,
            title='Help'
        )
        help_content = 'W-A-S-D - move \n' \
            'P - pause \n' \
            'LMB - attack \n' \
            'Mouse Wheel - zoom in and out \n' \
            'F - pick up items/interact \n' \
            'Q - exit \n' \
            '\n'
        self.help_menu.add.label(help_content)
        self.help_menu.add.button('Back', self.to_main)

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
        (str_value, fps_value), index_value = selected
        self.game.config.fps = fps_value
        self.show_apply()

    def on_resolution_change(self, selected, *args, **kwargs):
        (str_value, resolution_value), index_value = selected
        self.game.config.screen_resolution = resolution_value
        self.show_apply()

    def show_apply(self):
        if hasattr(self, 'apply_button'):
            self.apply_button.show()
        if hasattr(self, 'warning_label'):
            self.warning_label.show()

    def apply_changes(self):
        self.game.config.save()
        self.apply_button.hide()

    def to_settings(self):
        self.current_menu.disable()
        self.current_menu = self.settings_menu
        self.current_menu.enable()

    def to_main(self):
        self.current_menu.disable()
        self.current_menu = self.menu
        self.current_menu.enable()

    def to_help(self):
        self.current_menu.disable()
        self.current_menu = self.help_menu
        self.current_menu.enable()
