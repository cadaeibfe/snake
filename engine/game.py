import pygame
from pygame.locals import *

from statestack import StateStack

MAX_FPS = 60
MS_PER_FRAME = 1000 / 25.0

class Game(object):
    def __init__(self, title, window_size):
        '''Initializes everything for the game.'''
        pygame.mixer.pre_init(buffer=1024)
        pygame.init()

        # Set up a surface for the main window.
        window = pygame.display.set_mode(window_size)
        pygame.display.set_caption(title)

        # Set up a stack to manage game states.
        self.state_stack = StateStack(window)
        self.register_states()
        self.state_stack.push_state(self.get_start_state())

    def run(self):
        '''Runs the main game loop.'''
        clock = pygame.time.Clock()
        time_since_last_update = 0
        running = True

        while running:
            elapsed_time = clock.tick(MAX_FPS)
            time_since_last_update += elapsed_time

            while time_since_last_update >= MS_PER_FRAME:
                time_since_last_update -= MS_PER_FRAME 

                self.process_inputs()
                self.update(MS_PER_FRAME)

                # Exit the game if there are no active states.
                if self.state_stack.is_empty():
                    running = False

            self.draw()

        pygame.quit()

    def process_inputs(self):
        '''Passes events to the active states.'''
        for event in pygame.event.get():
            self.state_stack.handle_event(event)

            if self.is_trying_to_quit(event):
                self.state_stack.clear_states()

    def update(self, dt):
        '''Updates the active states to the next frame.'''
        self.state_stack.update(dt)

    def draw(self):
        '''Renders the current frame.'''
        self.state_stack.draw()
        pygame.display.update()

    def is_trying_to_quit(self, event):
        '''Checks if X box is clicked or Alt+F4 is pressed.'''
        keys_pressed = pygame.key.get_pressed()
        alt_pressed = keys_pressed[K_LALT] or keys_pressed[K_RALT]
        alt_f4 = event.type == KEYDOWN and event.key == K_F4 and alt_pressed
        return event.type == QUIT or alt_f4

    def register_states(self):
        '''Registers all possible states of the game.'''
        raise Exception('Unimplemented abstract method: register_states')

    def get_start_state(self):
        '''Returns the ID of the starting state.'''
        raise Exception('Unimplemented abstract method: get_start_state')
