
"""
GameEngine: owns the basket and all falling objects.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

MIN_SPAWN_INTERVAL = 35
MAX_SPAWN_INTERVAL = 65
MAX_OBJECTS_ON_SCREEN = 5
MIN_SPAWN_DISTANCE = 100
MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.last_spawn_x = None
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _spawn_object(self):
        if len(self.objects) >= MAX_OBJECTS_ON_SCREEN:
            return

        # Try to choose a location away from the previous spawn.
        possible_positions = [
            x for x in range(20, WIDTH - 19)
            if (
                self.last_spawn_x is None
                or abs(x - self.last_spawn_x) >= MIN_SPAWN_DISTANCE
            )
        ]

        if not possible_positions:
            x = random.randint(20, WIDTH - 20)
        else:
            x = random.choice(possible_positions)

        self.last_spawn_x = x
        self.objects.append(FallingObject(x=x, y=-14, speed=3))

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        if keys_pressed[pygame.K_LEFT]:
            self.basket.x -= self.basket.speed

        if keys_pressed[pygame.K_RIGHT]:
            self.basket.x += self.basket.speed

        # Keep the entire basket inside the screen.
        half_width = self.basket.width / 2
        self.basket.x = max(
            half_width,
            min(WIDTH - half_width, self.basket.x)
        )

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.__init__()

    def update(self):
        if self.game_over:
            return

        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:
            self._spawn_object()
            self.frames_until_spawn = random.randint(
                MIN_SPAWN_INTERVAL,
                MAX_SPAWN_INTERVAL
            )

        for obj in self.objects:
            obj.update()

        # Check catches without modifying the list while iterating.
        basket_rect = self.basket.get_rect()
        remaining_objects = []

        for obj in self.objects:
            if is_caught(basket_rect, obj):
                self.score += 1
            else:
                remaining_objects.append(obj)

        self.objects = remaining_objects

        # Remove missed objects and update the miss count.
        missed = [
            obj for obj in self.objects
            if obj.is_past_bottom(HEIGHT)
        ]

        if missed:
            self.objects = [
                obj for obj in self.objects
                if not obj.is_past_bottom(HEIGHT)
            ]

            self.misses += len(missed)

            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(
            surface, font, f"Score: {self.score}", (10, 10)
        )
        renderer.draw_text(
            surface, font,
            f"Misses: {self.misses}/{MAX_MISSES}",
            (10, 36)
        )

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"Game Over! Final score: {self.score}. Press R to restart."
            )