import pygame
from pygame.locals import *

from collections import namedtuple
from operator import itemgetter
import os.path

from engine.graphics import Text
from engine.gui import Container

from animation import ShutterAnimation
from constants import *
from resourceids import States
from textbox import TextBox

HighScore = namedtuple('HighScore', 'value, initials highlite')

class HighScoreState(object):
    def __init__(self, stack, window, last_score_value):
        '''Sets up the high score state.'''
        self.stack = stack
        self.window = window

        # Check if the score from the last game is a new high score.
        self.new_score = None
        if last_score_value:
            self.new_score = self.get_new_high_score(last_score_value[0])

        if self.new_score:
            # Create interface objects for the initials input screen.
            self.game_objects = self.build_initials_input_screen(window)
        else:
            # Create interface objects for the high score table screen.
            scores = self.load_high_scores(HIGH_SCORES_FILE)
            self.game_objects = self.build_high_scores_view_screen(window, scores)

    def build_initials_input_screen(self, window):
        '''Creates interface objects for the initials input screen.'''
        # Set up a title for the initials input screen.
        bigfont = pygame.font.SysFont('mono', 50)
        title = Text('New High Score', bigfont, MENU_TEXT_COLOR)

        # Set up an instructional message for the input screen.
        smallfont = pygame.font.SysFont('mono', 28)
        message = Text('Enter your initials', smallfont, MENU_TEXT_COLOR)

        # Set up a field to input the player's initials.
        self.initials_input = TextBox(smallfont, self.enter_initials)

        container = Container()
        container.pack(message)
        container.pack(self.initials_input)
        container.align_center()

        # Set up the animation object.
        return [ShutterAnimation(title, container, TEXT_SPEED, window)]

    def build_high_scores_view_screen(self, window, scores):
        '''Creates interface objects for the high scores view screen.'''
        # Set up a title for the high scores table.
        bigfont = pygame.font.SysFont('mono', 50)
        title = Text('Top 10 High Scores', bigfont, MENU_TEXT_COLOR)

        # Set up the text of the high score table.
        smallfont = pygame.font.SysFont('mono', 28)
        table = self.build_high_scores_table(smallfont, scores)

        # Add a continue message below the high score table.
        message = Text('Press space to continue', smallfont, MENU_TEXT_COLOR)
        container = Container()
        container.pack(table)
        container.pack(message)
        container.align_center()

        # Set up the animation object.
        return [ShutterAnimation(title, container, TEXT_SPEED, window)]
    
    def build_high_scores_table(self, font, scores):
        '''Returns a component displaying the top 10 high scores.'''
        table = Container()
        for i in range(10):
            # Create a text object for each score.
            initials = scores[i].initials if i < len(scores) else '---'
            value = scores[i].value if i < len(scores) else 0
            color = (255, 0, 0) if i < len(scores) and scores[i].highlite else MENU_TEXT_COLOR
            table.pack(Text('%-3s %3s  %5s' % (str(i + 1) + '.', initials, value), font, color))
        return table

    def get_new_high_score(self, last_score_value):
        '''Returns the score value from the last game if it is high
        enough to be one of the top 10 high scores, otherwise None'''
        # Get a list of the current high score values.
        scores = self.load_high_scores(HIGH_SCORES_FILE)
        old_score_values = [score.value for score in scores]

        # Add the new value and check if it's in the top 10.
        new_score_values = old_score_values[:]
        new_score_values.append(last_score_value)
        new_score_values = sorted(new_score_values, reverse=True)[:10]

        if new_score_values != old_score_values:
            return last_score_value
        else:
            return None

    def enter_initials(self, initials):
        '''Called when the user is finished entering their initials.'''

        # Add the new score value with its associated initials to
        # the high score list.
        scores = self.load_high_scores(HIGH_SCORES_FILE)
        scores.append(HighScore(self.new_score, initials, True))
        scores = sorted(scores, key=itemgetter(0), reverse=True)[:10]

        # Save the updated scores to disk.
        self.save_high_scores(HIGH_SCORES_FILE, scores)

        # Proceed to the high scores view screen.
        self.new_score = None
        self.game_objects = self.build_high_scores_view_screen(self.window, scores)

    def load_high_scores(self, filename):
        '''Loads the high scores from the given file.'''
        high_scores = []

        if os.path.exists(filename):
            with open(filename) as f:
                for line in f:
                    parts = line.split()
                    score = HighScore(int(parts[1]), parts[0], False)
                    high_scores.append(score)

        return high_scores

    def save_high_scores(self, filename, high_scores):
        '''Saves the high scores to the given file.'''
        with open(filename, 'w') as f:
            for score in high_scores:
                f.write('%s %s\n' % (score.initials, score.value))

    def handle_event(self, event):
        '''Handles events for the high score table.'''
        if self.new_score:
            # Handles the initials input screen.
            if event.type == KEYDOWN:
                self.initials_input.handle_key(event.key)
        else:
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    # Return the main menu when space is pressed.
                    self.stack.pop_state()
                    self.stack.push_state(States.Menu)
                elif event.key == K_ESCAPE:
                    # Exit if escape is pressed.
                    self.stack.clear_states()

        return False

    def update(self, dt):
        '''Updates the high score table.'''
        for game_object in self.game_objects:
            game_object.update(dt)

        # Make sure the cursor on the input box blinks.
        # TODO: should ShutterAnimation update its components?
        if self.new_score:
            self.initials_input.update(dt)

        return False

    def draw(self):
        '''Draws the high score table.'''
        window = self.window
        window.fill(BACKGROUND_COLOR)
        for game_object in self.game_objects:
            game_object.draw(window)
