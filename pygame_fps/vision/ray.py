from typing import Tuple, Iterator, Optional

from numpy import ndarray, array, cos, sin, ceil, tan, floor

from pygame_fps.player.angle import Angle
from pygame_fps.stage import Stage


class VisionRay:
    def __init__(self, start: ndarray, end: ndarray, max_length: float, direction_relative: Angle):
        self._start = start
        self._end = end
        self._max_length = max_length
        self._direction_relative = direction_relative

        self._length_lazy: Optional[float] = None

    @classmethod
    def to_direction(cls, position: ndarray, direction: Angle, direction_relative: Angle, stage: Stage,
                     length_limit: float) -> 'VisionRay':
        position = position.copy()
        end = _find_farthest_point(position, direction.rotate(direction_relative), stage, length_limit)
        return VisionRay(position, end, length_limit, direction_relative)

    @property
    def start(self) -> ndarray:
        return self._start

    @property
    def end(self) -> ndarray:
        return self._end

    @property
    def direction_relative(self) -> Angle:
        return self._direction_relative

    @property
    def length(self) -> float:
        if self._length_lazy is None:
            self._length_lazy = sum((self.start - self.end) ** 2) ** 0.5
        return self._length_lazy

    @property
    def max_length(self) -> float:
        return self._max_length

    @property
    def is_max_length(self) -> bool:
        return abs(self.max_length - self.length) <= 1e-4


def _find_farthest_point(position: ndarray, direction: Angle, stage: Stage, length_limit: float) -> ndarray:
    length_limit2 = length_limit**2
    for point, dist2 in _iterate_nearest_intersection_points(position, direction):
        if length_limit2 <= dist2:
            return position + length_limit * array([cos(float(direction)), sin(float(direction))])
        if _is_blocked(point, direction, stage):
            return point


def _iterate_nearest_intersection_points(position: ndarray, direction: Angle) -> Iterator[Tuple[ndarray, float]]:
    x_intercept = _iter_intersection_points_in_x_direction(position, direction)
    y_intercept = _iter_intersection_points_in_y_direction(position, direction)

    x_intercept_dist2, y_intercept_dist2 = float('inf'), float('inf')
    x_intercept_point, y_intercept_point = None, None

    while True:
        if x_intercept_point is None:
            x_intercept_point, x_intercept_dist2 = _visit_intersection(position, x_intercept)

        if y_intercept_point is None:
            y_intercept_point, y_intercept_dist2 = _visit_intersection(position, y_intercept)

        if y_intercept_point is None or x_intercept_dist2 <= y_intercept_dist2:
            yield x_intercept_point, x_intercept_dist2
            x_intercept_point = None
        else:
            yield y_intercept_point, y_intercept_dist2
            y_intercept_point = None


def _visit_intersection(position, intercept_iter) -> (ndarray, float, bool):
    try:
        point = next(intercept_iter)
    except StopIteration:
        return None, None
    farthest_dist2 = _distance2(position, point)
    return point, farthest_dist2


def _is_blocked(point: ndarray, direction: Angle, stage: Stage) -> bool:
    x, y = point
    if abs(x - floor(x)) <= 1e-7:
        if cos(float(direction)) > 0:
            if stage.has_block(x, floor(y)):
                return True
        elif stage.has_block(x-1, floor(y)):
            return True
    if abs(y - floor(y)) <= 1e-7:
        if sin(float(direction)) > 0:
            if stage.has_block(floor(x), y):
                return True
        elif stage.has_block(floor(x), y-1):
            return True
    return False


def _iter_intersection_points_in_x_direction(position: ndarray, direction: Angle) -> Iterator[ndarray]:
    cos_theta = cos(float(direction))
    if cos_theta == 0:
        return

    x0, y0 = position
    tan_theta = tan(float(direction))
    for y, x in _iter_line_intersection(tan_theta, y0, x0, cos_theta > 0):
        yield x, y


def _iter_intersection_points_in_y_direction(position: ndarray, direction: Angle) -> Iterator[ndarray]:
    sin_theta = sin(float(direction))
    if sin_theta == 0:
        return

    x0, y0 = position
    cot_theta = cos(float(direction))/sin_theta
    yield from _iter_line_intersection(cot_theta, x0, y0, sin_theta > 0)


def _iter_line_intersection(m, p0, q0, positive):
    q = ceil(q0) if positive else floor(q0)
    while True:
        p = p0 + (q - q0) * m
        yield array([p, q])
        q += 1 if positive else -1


def _distance2(a: ndarray, b: ndarray) -> float:
    return sum((a - b) ** 2)
