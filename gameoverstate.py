import pygame
from pygame.locals import *

from engine.graphics import Text

from animation import ShutterAnimation
from constants import *
from resourceids import States

class GameOverState(object):
    def __init__(self, stack, window, last_score):
        '''Sets up the game over screen.'''
        self.stack = stack
        self.window = window
        self.last_score = last_score

        # Set up the game over message.
        bigfont = pygame.font.SysFont('mono', 100)
        gameover = Text('Game Over', bigfont, MENU_TEXT_COLOR)

        # Set up a continue message.
        smallfont = pygame.font.SysFont('mono', 28)
        message = Text('Press space to continue', smallfont, MENU_TEXT_COLOR)

        # Set up animation objects to move the texts into place.
        self.game_objects = []
        self.game_objects.append(ShutterAnimation(gameover, message, TEXT_SPEED, window))

    def handle_event(self, event):
        '''Handles events for the game over screen.'''
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                # Continue to the high score display when space is pressed.
                self.stack.pop_state()
                self.stack.pop_state()
                self.stack.push_state(States.HighScore, *self.last_score)
            elif event.key == K_ESCAPE:
                # Exit if escape is pressed.
                self.stack.clear_states()

        return False

    def update(self, dt):
        '''Updates the game over screen.'''
        for game_object in self.game_objects:
            game_object.update(dt)

        return False

    def draw(self):
        '''Draws the game over screen.'''
        window = self.window
        for game_object in self.game_objects:
            game_object.draw(window)
