import pygame
from pygame.locals import *

from engine.graphics import Text

from animation import ShutterAnimation
from constants import *
from resourceids import States

class MenuState(object):
    def __init__(self, stack, window, unused_args):
        '''Sets up the main menu screen.'''
        self.stack = stack
        self.window = window

        # Set up the title text.
        bigfont = pygame.font.SysFont('mono', 100)
        title = Text('Snake', bigfont, MENU_TEXT_COLOR)

        # Set up a start message.
        smallfont = pygame.font.SysFont('mono', 28)
        start = Text('Press any key to start', smallfont, MENU_TEXT_COLOR)

        # Set up an animation object to move the texts into place.
        self.game_objects = []
        self.game_objects.append(ShutterAnimation(title, start, TEXT_SPEED, window))


    def handle_event(self, event):
        '''Handles events for the main menu screen.'''
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                # Exit if escape is pressed.
                self.stack.clear_states()
            else:
                # Start the game if any other key is pressed.
                self.stack.pop_state()
                self.stack.push_state(States.Play)

        return True

    def update(self, dt):
        '''Updates the main menu screen.'''
        for game_object in self.game_objects:
            game_object.update(dt)

        return True

    def draw(self):
        '''Draws the main menu screen.'''
        window = self.window
        window.fill(BACKGROUND_COLOR)
        for game_object in self.game_objects:
            game_object.draw(window)
