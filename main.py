from numpy import pi

from stage_layout import stage_layout
from pygame_fps.first_person_view.panel import FirstPersonViewPanel
from pygame_fps.player.angle import Angle
from pygame_fps.pygame import PygameLoop
from pygame_fps.player.main import MainPlayer
from pygame_fps.stage import Stage
from pygame_fps.top_view.panel import TopViewPanel
from pygame_fps.vision.field import VisionField


def main():
    stage = Stage(stage_layout)
    player = MainPlayer(
        3, 3, Angle(0.0),
        turn_radian=pi/90, move_distance=0.1,
    )
    vision = VisionField(
        player, stage,
        fov=60/180*pi, n_rays=120, ray_length=20,
    )

    first_person_view = FirstPersonViewPanel(
        (50, 100, 1050, 500), vision,
        wall_height=2.5, player_height=1.75, vertical_fov=120/180*pi,
    )
    top_view = TopViewPanel((50, 50, 250, 125), player, stage, vision)

    loop = PygameLoop((1150, 700), frame_rate=30)
    loop.add_game_object(player)
    loop.add_game_object(vision)
    loop.add_game_object(first_person_view)
    loop.add_game_object(top_view)
    loop.start()


if __name__ == '__main__':
    main()
