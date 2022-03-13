from typing import Union

import numpy as np


class Angle:
    def __init__(self, angle: float):
        self._angle = angle

    def rotate(self, rad: Union['Angle', float]) -> 'Angle':
        if isinstance(rad, Angle):
            rad = float(rad)
        angle = self._angle + rad
        angle %= 2*np.pi
        return Angle(angle)

    def __float__(self) -> float:
        return float(self._angle)
