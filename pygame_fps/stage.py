from typing import List


class Stage:
    def __init__(self, layout: List[str]):
        width = len(layout[0])
        assert set(set(line) - {'.', 'x'} == set() for line in layout)
        assert all(len(line) == width for line in layout)

        self._layout = layout
        self._height = len(layout)
        self._width = width

    def has_block(self, x: int, y: int) -> bool:
        if not self._is_inside_stage(x, y):
            return True

        return self._layout[int(y)][int(x)] == 'x'

    def _is_inside_stage(self, x: int, y: int) -> bool:
        return 0 <= x < self._width and 0 < y < self._height

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height
