from src.game_object.actor import Actor


class Container(Actor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
