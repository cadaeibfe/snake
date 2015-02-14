import pygame

from engine.graphics import Text

from constants import *

class Score(object):
    def __init__(self):
        font = pygame.font.SysFont('mono', 28)
        self.value = 0
        self.text = Text('Score: 0', font, SCORE_TEXT_COLOR)

        # Place the score display in the top left corner.
        self.text.set_position((5, 5))

    def increase(self, amount):
        '''Increase the score and update the text display.'''
        self.value += amount
        self.text.set_string('Score: ' + str(self.value))

    def update(self, dt):
        pass

    def draw(self, window):
        '''Draws the current score to the window.'''
        self.text.draw(window)
