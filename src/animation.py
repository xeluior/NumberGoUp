from math import floor

import pygame.surface


class Animation:
    def __init__(self, keyframes: [pygame.surface.Surface], framerate: int = 60, repeat: bool = False):
        self.keyframes = keyframes
        self.framerate = framerate
        self.repeat = repeat
        self.stopped = True
        self.last_frame = 0
        self.play_time = 0

    def stop(self) -> None:
        self.stopped = True

    def reset(self) -> None:
        self.play_time = 0
        self.last_frame = 0

    def start(self) -> None:
        self.stopped = False

    def restart(self) -> None:
        self.reset()
        self.start()

    def length(self) -> float:
        return len(self.keyframes) * 1000 / self.framerate

    def frame_advance(self, time_increment: int) -> pygame.surface.Surface:
        if self.stopped:
            return self.keyframes[self.last_frame]

        self.play_time += time_increment

        if self.play_time >= self.length():
            if self.repeat:
                self.play_time %= self.length()
            else:
                self.stop()
                return self.keyframes[self.last_frame]

        self.last_frame = floor(self.play_time / 1000 * self.framerate)
        return self.keyframes[self.last_frame]


class AnimationController:
    def __init__(self, animations: {str: Animation}, default_anim: str):
        self.animations: {str: Animation} = animations
        self.active_anim: Animation = self.animations[default_anim]

    def play(self, animation: str):
        self.active_anim = self.animations[animation]
        self.active_anim.restart()

    def frame_advance(self, time_increment: int) -> pygame.surface.Surface:
        return self.active_anim.frame_advance(time_increment)

    def stop(self):
        self.active_anim.stop()
