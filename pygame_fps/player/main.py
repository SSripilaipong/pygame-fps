from typing import Any

from numpy import pi, array, cos, sin, ndarray

from pygame_fps.game import GameObject, GameLoop
from pygame_fps.game.key import Key
from pygame_fps.player.angle import Angle


class MainPlayer(GameObject):
    def __init__(self, x: float, y: float, heading: Angle, turn_radian: float, move_distance: float):
        self._position = array([x, y], dtype=float)
        self._heading = heading or Angle(0)
        self._turn_radian = turn_radian
        self._move_distance = move_distance

    def on_added_to_game_loop(self, loop: GameLoop):
        subscribing_keys = [Key.LEFT, Key.RIGHT, Key.w, Key.a, Key.s, Key.d]
        for key in subscribing_keys:
            loop.subscribe_for_pressed_keys(key, self)

    def turn_left(self):
        self._heading = self._heading.rotate(-self._turn_radian)

    def turn_right(self):
        self._heading = self._heading.rotate(+self._turn_radian)

    def move_forward(self):
        self._move_in_direction(float(self._heading))

    def move_left(self):
        self._move_in_direction(float(self._heading) - pi/2)

    def move_backward(self):
        self._move_in_direction(float(self._heading) + pi)

    def move_right(self):
        self._move_in_direction(float(self._heading) + pi/2)

    def on_key_pressed(self, key: Key):
        if key == Key.LEFT:
            self.turn_left()
        elif key == Key.RIGHT:
            self.turn_right()
        elif key == Key.w:
            self.move_forward()
        elif key == Key.a:
            self.move_left()
        elif key == Key.s:
            self.move_backward()
        elif key == Key.d:
            self.move_right()

    def _move_in_direction(self, direction: float):
        displacement = self._move_distance * array([cos(direction), sin(direction)])
        self._position += displacement

    @property
    def position(self) -> ndarray:
        return self._position

    @property
    def heading(self) -> Angle:
        return self._heading

    def draw(self, display: Any):
        pass

    def update(self):
        pass
