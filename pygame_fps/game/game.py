from abc import ABC, abstractmethod
from typing import List, Any, Set, Dict

from pygame_fps.game.key import Key


class GameObject(ABC):
    def on_added_to_game_loop(self, loop: 'GameLoop'):
        pass

    def on_key_pressed(self, key: Key):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, display: Any):
        pass


class GameLoop(ABC):
    def __init__(self):
        self._game_objects: List[GameObject] = []
        self._key_subscriptions: Dict[Key, List[GameObject]] = {}

    def subscribe_for_pressed_keys(self, key: Key, obj: GameObject):
        self._key_subscriptions[key] = self._key_subscriptions.get(key, []) + [obj]

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def is_running(self) -> bool:
        pass

    @abstractmethod
    def get_pressed_keys(self) -> Set[Key]:
        pass

    @abstractmethod
    def get_display(self) -> Any:
        pass

    @abstractmethod
    def on_frame_ended(self):
        pass

    def start(self):
        self.setup()

        while not self.is_running():
            self._handle_events()

            self.update_all()
            self.draw_all()
            self.on_frame_ended()

    def _handle_events(self):
        pressed_keys = self.get_pressed_keys()
        self._handle_pressed_keys(pressed_keys)

    def _handle_pressed_keys(self, keys: Set[Key]):
        for key in keys:
            for obj in self._key_subscriptions[key]:
                obj.on_key_pressed(key)

    def add_game_object(self, obj: GameObject):
        self._game_objects.append(obj)
        obj.on_added_to_game_loop(self)

    def update_all(self):
        for obj in self._game_objects:
            obj.update()

    def draw_all(self):
        display = self.get_display()
        for obj in self._game_objects:
            obj.draw(display)
