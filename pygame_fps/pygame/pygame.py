from typing import Optional, Any, Tuple, Set

import pygame

from pygame_fps.game import GameLoop
from pygame_fps.game.key import Key
from pygame_fps.pygame.key_mapper import key_mapper


class PygameLoop(GameLoop):
    def __init__(self, size: Tuple[int, int], frame_rate: int):
        super().__init__()
        self._size = size
        self._frame_rate = frame_rate
        self._clock = pygame.time.Clock()
        self._display: Optional[pygame.Surface] = None

    def setup(self):
        pygame.init()
        self._display = pygame.display.set_mode(self._size)

    def is_running(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
        return False

    def get_pressed_keys(self) -> Set[Key]:
        pygame_keys = pygame.key.get_pressed()

        pressed_keys = set()
        for pygame_key, game_key in key_mapper.items():
            if pygame_keys[pygame_key]:
                pressed_keys.add(game_key)

        return pressed_keys

    def get_display(self) -> Any:
        return self._display

    def draw_all(self):
        self._display.fill('black')
        super().draw_all()

    def on_frame_ended(self):
        self._clock.tick(self._frame_rate)
        pygame.display.update()
