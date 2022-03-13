from itertools import product
from typing import Any, Tuple

import pygame.draw
from numpy import floor, ceil, array, ndarray
from pygame import Surface

from pygame_fps.game import GameObject
from pygame_fps.player.main import MainPlayer
from pygame_fps.stage import Stage
from pygame_fps.vision.field import VisionField


class TopViewPanel(GameObject):
    def __init__(self, draw_area_px: Tuple[int, int, int, int], player: MainPlayer, stage: Stage, vision: VisionField):
        self._draw_area_px = draw_area_px
        self._player = player
        self._stage = stage
        self._vision = vision

        self._offset_px = array(self._draw_area_px[:2])
        self._width_px = self._draw_area_px[2]
        self._height_px = self._draw_area_px[3]
        self._block_size_px = array([self._width_px/self._stage.width, self._height_px/self._stage.height])

    def draw(self, display: Any):
        assert isinstance(display, Surface)
        self._draw_stage(display)
        self._draw_vision(display)
        self._draw_player(display)

    def _draw_stage(self, display: Surface):
        pygame.draw.rect(display, 'black', self._draw_area_px)

        for y, x in product(range(self._stage.height), range(self._stage.width)):
            if self._stage.has_block(x, y):
                pos_px = self._pos_to_px(array([x, y]))
                rect = (*floor(pos_px), *ceil(self._block_size_px))
                pygame.draw.rect(display, 'white', rect)

    def _draw_vision(self, display: Surface):
        for ray in self._vision.rays:
            pygame.draw.line(display, 'green', tuple(self._pos_to_px(ray.start)), tuple(self._pos_to_px(ray.end)))

    def _draw_player(self, display: Surface):
        pygame.draw.circle(display, 'yellow', tuple(self.player_pos_px), self._draw_area_px[2]/50)

    @property
    def player_pos_px(self) -> ndarray:
        return self._pos_to_px(self._player.position)

    def _pos_to_px(self, pos: ndarray) -> ndarray:
        return self._offset_px + pos * self._block_size_px

    def update(self):
        pass
