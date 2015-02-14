import pygame
from pygame.locals import *

from constants import *
from input import InputHandler
from map import Map
from resourceids import Sounds, States, Textures
from score import Score
from snake import Snake

class PlayState(object):
    def __init__(self, stack, window, unused_args):
        '''Sets up the start of a new game.'''
        self.stack = stack
        self.window = window

        self.game_objects = []

        # The player's score is initially zero. Make this the firsat
        # game object so that it will be drawn underneath other objects.
        self.score = Score()
        self.game_objects.append(self.score)

        # Load textures used by the game.
        self.textures = {}
        self.textures[Textures.Snake] = pygame.image.load('assets/segments.png')
        self.textures[Textures.Apple] = pygame.image.load('assets/apple.png')

        # Set up the map object.
        columns = window.get_size()[0] / TILE_SIZE
        rows = window.get_size()[1] / TILE_SIZE
        self.map = Map(columns, rows, self.textures)
        self.game_objects.append(self.map)

        # Set up the snake object.
        self.snake = Snake(self.map, self.textures)
        self.snake.eat_callback = self.notify_apple_was_eaten
        self.snake.crash_callback = self.notify_snake_crashed
        self.game_objects.append(self.snake)

        # Set up an object to control the snake through player input.
        self.input_handler = InputHandler(INPUT_MAPPING_FILE)

        # Spawn an apple for the snake to eat.
        self.map.spawn_apple(self.snake)

        # Load sounds used by the game.
        self.sounds = {}
        self.sounds[Sounds.Crash] = pygame.mixer.Sound('assets/crash.wav')
        self.sounds[Sounds.Eat] = pygame.mixer.Sound('assets/eat.wav')

    def handle_event(self, event):
        '''Changes the snake's direction based on user input.'''
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.stack.push_state(States.Pause)

        command = self.input_handler.handle_event(event)
        if command is not None:
            command.execute(self.snake)
        return True

    def update(self, dt):
        '''Updates the game for the next frame.'''
        for game_object in self.game_objects:
            game_object.update(dt)

        return True

    def draw(self):
        '''Draws the current state of the game.'''
        window = self.window
        window.fill(BACKGROUND_COLOR)

        for game_object in self.game_objects:
            game_object.draw(window)

    def notify_apple_was_eaten(self):
        '''Called when the head of the snake hits the apple.'''
        self.sounds[Sounds.Eat].play()
        self.score.increase(APPLE_POINT_VALUE)
        self.map.spawn_apple(self.snake)

    def notify_snake_crashed(self):
        '''Called when the snake crashes into a wall or itself.'''
        self.sounds[Sounds.Crash].play()
        self.stack.push_state(States.GameOver, self.score.value)
