from typing import Any, List, Iterator

from numpy import linspace, ndarray

from pygame_fps.game import GameObject
from pygame_fps.player.angle import Angle
from pygame_fps.player.main import MainPlayer
from pygame_fps.stage import Stage
from pygame_fps.vision.ray import VisionRay


class VisionField(GameObject):
    def __init__(self, player: MainPlayer, stage: Stage, fov: float, n_rays: int, ray_length: float):
        self._player = player
        self._stage = stage
        self._n_rays = n_rays
        self._ray_length = ray_length

        self._rotate_range = linspace(-fov/2, +fov/2, n_rays)
        self._rays: List[VisionRay] = []

    @property
    def rays(self) -> Iterator[VisionRay]:
        for ray in self._rays:
            yield ray

    def update(self):
        self._rays = [VisionRay.to_direction(self.position, self.direction, Angle(rot), self._stage, self._ray_length)
                      for rot in self._rotate_range]

    @property
    def n_rays(self) -> int:
        return self._n_rays

    @property
    def position(self) -> ndarray:
        return self._player.position

    @property
    def direction(self) -> Angle:
        return self._player.heading

    def draw(self, display: Any):
        pass
