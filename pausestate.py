import pygame
from pygame.locals import *

from engine.graphics import Text
from engine.gui import Container

from animation import ShutterAnimation
from constants import *

class PauseState(object):
    def __init__(self, stack, window, unused_args):
        '''Sets up the pause screen.'''
        self.stack = stack
        self.window = window

        # Set up the pause screen title.
        bigfont = pygame.font.SysFont('mono', 100)
        title = Text('Paused', bigfont, MENU_TEXT_COLOR)

        # Set up an animation object to move the texts into place.
        self.game_objects = []
        self.game_objects.append(ShutterAnimation(title, Container(), TEXT_SPEED, window))

    def handle_event(self, event):
        '''Handles events for the pause screen.'''
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                # Unpause if the escape key is pressed.
                self.stack.pop_state()

        return False

    def update(self, dt):
        '''Updates the pause screen.'''
        for game_object in self.game_objects:
            game_object.update(dt)

        return False

    def draw(self):
        '''Draws the pause screen.'''
        window = self.window

        for game_object in self.game_objects:
            game_object.draw(window)
