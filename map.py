import pygame

from itertools import product
from random import choice

from constants import *
from resourceids import Textures
from segment import draw_segment

class Map(object):
    def __init__(self, columns, rows, textures):
        '''Creates a new map with the given dimensions.'''
        self.columns = columns
        self.rows = rows
        self.apple = None
        self.apple_image = textures[Textures.Apple]

    def spawn_apple(self, snake):
        '''Places the apple at a random position which doesn't
        lie on the snake.'''
        self.apple = choice([p for p in product(range(self.columns), range(self.rows)) if p not in snake.segments])

    def get_starting_pos(self):
        '''Returns the location where the snake enters the map.'''
        return (self.columns / 2, self.rows / 2)

    def out_of_bounds(self, point):
        '''Returns true if the given point is outside the bounds
        of this map.'''
        return (point[0] < 0 or point[0] >= self.columns or
                point[1] < 0 or point[1] >= self.rows)

    def update(self, dt):
        pass

    def draw(self, window):
        '''Draws the map.'''
        # Calculate the position of the apple on screen.
        x = self.apple[0] * TILE_SIZE
        y = self.apple[1] * TILE_SIZE

        # Blit the image.
        window.blit(self.apple_image, (x, y))
