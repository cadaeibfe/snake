import pygame

from constants import *

def draw_segment(window, position, color):
    '''Draws a colored box with a black outline.'''
    rect = (position[0] * TILE_SIZE + 1, position[1] * TILE_SIZE + 1,
            TILE_SIZE - 2, TILE_SIZE - 2)
    pygame.draw.rect(window, color, rect)
    pygame.draw.rect(window, OUTLINE_COLOR, rect, 1)

