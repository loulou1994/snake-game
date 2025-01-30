from typing import List
from random import randint

import pygame as pg
from pygame.math import Vector2

SCREENRECT = pg.Rect(0, 0, 600, 450)
SNAKE_SEGMENT_SIZE = 20
BALL_SIZE = 20
DIRECTIONS = {
    pg.K_UP: Vector2(0, -1),
    pg.K_DOWN: Vector2(0, 1),
    pg.K_LEFT: Vector2(-1, 0),
    pg.K_RIGHT: Vector2(1, 0)
}

class Ball(pg.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.image = pg.Surface((BALL_SIZE, BALL_SIZE))
        self.rect = self.image.get_rect()

    def update(self):
        for coord in {"x": SCREENRECT.x, "y": SCREENRECT.y}:
            self.rect[coord] = randint(0, SCREENRECT[coord])

class Snake_Segment(pg.sprite.Sprite):

    def __init__(self, initial_pos: Vector2, size: int, *args, **kwargs):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.rect = self.image.fill((0, 255, 0))
        self.position = initial_pos
        self.rect.topleft = tuple(self.position)  # type: ignore

    def update(self, new_position: Vector2):
        self.position = new_position
        self.rect.topleft = tuple(self.position)  # type: ignore


class Snake(pg.sprite.RenderUpdates):
    _segments: List

    def __init__(self, head_pos: Vector2, size: int, length: int = 3):
        super().__init__()
        self._size = size
        self._head_pos = head_pos
        self._segments = []
        self._direction = Vector2(1, 0)  # right direction

        for x in range(length):
            segment_pos = Vector2(
                self._head_pos.x - (x * self._size), self._head_pos.y
            )
            segment = Snake_Segment(segment_pos, self._size)
            self._segments.append(segment)
            self.add(segment)

    def move(self) -> None:
        old_positions = [segment.position.copy() for segment in self._segments]

        head = self._segments[0]
        head.update(head.position + self._direction * self._size)

        for i in range(1, len(old_positions)):
            self._segments[i].update(old_positions[i-1])

    def grow(self) -> None:
        last_segment = self._segments[-1]
        second_to_last = self._segments[-2] if len(
            self._segments) > 1 else None

        if second_to_last:
            direction = last_segment.position - second_to_last.position
            new_pos = last_segment.position + direction * self._size
        else:
            new_pos = last_segment - self._direction * self._size

        new_last_segment = Snake_Segment(new_pos, self._size)
        self._segments.append(new_last_segment)
        self.add(new_last_segment)

    def set_direction(self, new_direction: Vector2) -> None:
        self._direction = new_direction

    def check_collision(self) -> bool:
        head_segment = self._segments[0]

        for snake_segment in self._segments[1:]:
            if head_segment.rect.colliderect(snake_segment.rect):
                return True
        return False


def main():
    if not pg.image.get_extended():
        raise SystemExit("Sorry, extended image module required")

    if pg.get_sdl_version()[0] == 2:
        pg.mixer.pre_init(44100, 32, 2, 1024)

    pg.init()

    if pg.mixer and not pg.mixer.get_init():
        print("Warning, no sound")
        pg.mixer = None

    screen = pg.display.set_mode(SCREENRECT.size)

    background = pg.Surface(SCREENRECT.size)
    background.fill("white")

    screen.blit(background, (0, 0))
    pg.display.flip()

    clock = pg.time.Clock()

    snake = Snake(Vector2(90, 90), SNAKE_SEGMENT_SIZE)
    
    # to draw the single ball
    single_ball = pg.sprite.GroupSingle()

    # print(snake.sprites())
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                exit(0)

            if event.type == pg.QUIT:
                exit(0)

            if event.type == pg.KEYDOWN and event.key in DIRECTIONS:
                new_direction = DIRECTIONS[event.key]
                snake.set_direction(new_direction)

        snake.clear(screen, background)
                
        snake.move()

        dirt_rect = snake.draw(screen)

        pg.display.update(dirt_rect)

        clock.tick(8)


main()