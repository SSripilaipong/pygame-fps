from typing import Any, Tuple

import numpy as np
import pygame.draw
from numpy import cos, tan, floor, array
from numpy.ma import arctan2, ceil
from pygame import Surface

from pygame_fps.game import GameObject
from pygame_fps.vision.field import VisionField
from pygame_fps.vision.ray import VisionRay


class FirstPersonViewPanel(GameObject):
    def __init__(self, draw_area_px: Tuple[int, int, int, int], vision: VisionField,
                 wall_height: float, player_height: float, vertical_fov: float):
        self._draw_area_px = draw_area_px
        self._vision = vision
        self._wall_height = wall_height
        self._player_height = player_height
        self._vertical_fov = vertical_fov

        self._wall_width = self._draw_area_px[2] / self._vision.n_rays

    def draw(self, display: Any):
        assert isinstance(display, Surface)
        pygame.draw.rect(display, (10, 10, 10), self._draw_area_px)
        for i, ray in enumerate(self._vision.rays):
            self._draw_wall_from_raw(display, i, ray)

    def _draw_wall_from_raw(self, display: Surface, index: int, ray: VisionRay):
        if ray.is_max_length:
            return

        wall_distance = ray.length*cos(float(ray.direction_relative))
        max_half_wall_height = tan(self._vertical_fov/2) * wall_distance
        if max_half_wall_height == 0:
            upper_wall_height_percent, lower_wall_height_percent = 1, 1
        else:
            upper_wall_height_percent = min((self._wall_height-self._player_height)/max_half_wall_height, 1)
            lower_wall_height_percent = min(self._player_height/max_half_wall_height, 1)

        upper_wall_height_px = upper_wall_height_percent * self.draw_area_height_px/2
        lower_wall_height_px = lower_wall_height_percent * self.draw_area_height_px/2

        height_px = lower_wall_height_px + upper_wall_height_px
        width_px = self._wall_width
        y_px = self._draw_area_px[1] + self.draw_area_height_px/2 - upper_wall_height_px
        x_px = self._draw_area_px[0] + index * self._wall_width

        color = array([10, 10, 10]) + array([245.0, 245.0, 245.0]) * (ray.max_length - ray.length)/ray.max_length
        pygame.draw.rect(display, color, (floor(x_px), floor(y_px), ceil(width_px), ceil(height_px)))

    @property
    def draw_area_height_px(self) -> float:
        return self._draw_area_px[3]

    @property
    def n_walls(self) -> int:
        return self._vision.n_rays

    def update(self):
        pass
