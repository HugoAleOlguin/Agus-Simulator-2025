class BaseMode:
    def __init__(self, screen, clock, WIDTH, HEIGHT, player_image, emoji_image, resources=None):
        self.screen = screen
        self.clock = clock
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.player_image = player_image
        self.emoji_image = emoji_image
        self.resources = resources

    def run_mode(self):
        raise NotImplementedError("El modo debe implementar el método run_mode.")
