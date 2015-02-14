from engine.game import Game

from gameoverstate import GameOverState
from highscorestate import HighScoreState
from menustate import MenuState
from pausestate import PauseState
from playstate import PlayState
from resourceids import States

class SnakeGame(Game):
    def __init__(self):
        super(SnakeGame, self).__init__('Snake', (640, 480))

    def register_states(self):
        '''Registers all possible states of the game.'''
        self.state_stack.register_state(States.Menu, MenuState)
        self.state_stack.register_state(States.Play, PlayState)
        self.state_stack.register_state(States.GameOver, GameOverState)
        self.state_stack.register_state(States.HighScore, HighScoreState)
        self.state_stack.register_state(States.Pause, PauseState)

    def get_start_state(self):
        '''Returns the ID of the starting state.'''
        return States.Menu
