from pygame.locals import *

import os.path

from engine.utility import enum

Action = enum('Action', 'MoveRight MoveLeft MoveUp MoveDown')

class InputHandler(object):
    def __init__(self, filename):
        '''Sets up the key mappings for the game.'''
        self.key_mapping = self.load_key_mapping(filename)

        self.action_mapping = {
                Action.MoveRight: ChangeDirectionCommand((1, 0)),
                Action.MoveLeft: ChangeDirectionCommand((-1, 0)),
                Action.MoveUp: ChangeDirectionCommand((0, -1)),
                Action.MoveDown: ChangeDirectionCommand((0, 1))
                }

    def load_key_mapping(self, filename):
        '''Loads the key mapping from a file, or use the defaults
        if the file doesn't exist.'''
        key_mapping = self.get_default_key_mapping()

        if os.path.exists(filename):
            with open(filename) as f:
                for line in f:
                    try:
                        parts = line.split()
                        key = globals()[parts[0]]
                        action = getattr(Action, parts[1])
                        key_mapping[key] = action
                    except:
                        # Exception occurred, fall back on default.
                        pass

        return key_mapping

    def get_default_key_mapping(self):
        return {
                K_RIGHT: Action.MoveRight,
                K_LEFT: Action.MoveLeft,
                K_UP: Action.MoveUp,
                K_DOWN: Action.MoveDown
                }

    def handle_event(self, event):
        '''Returns a command mapped to the given input, or None.'''
        if event.type == KEYDOWN:
            action = self.key_mapping.get(event.key, None)
            if action is not None:
                return self.action_mapping[action]

        # Not a recognized input, so return nothing.
        return None

class ChangeDirectionCommand(object):
    '''A command object which changes an actor's direction.'''

    def __init__(self, new_direction):
        self.new_direction = new_direction

    def execute(self, actor):
        actor.direction_buffer.append(self.new_direction)
