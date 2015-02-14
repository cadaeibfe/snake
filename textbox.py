import pygame
from pygame.locals import *

from string import lowercase

from engine.graphics import Transformable, Text
from engine.timer import Timer

from constants import *

class TextBox(Transformable):
    def __init__(self, font, callback):
        self.font = font
        self.callback = callback
        self.text = Text('', font, MENU_TEXT_COLOR)
        self.text.set_parent_transform(self)
        self.cursor = 0
        self.cursor_on = True
        self.blink_timer = Timer(300, self.toggle_blink)

    def handle_key(self, key):
        if key < 256 and chr(key) in lowercase and self.cursor < 3:
            # Add a new letter and advance the cursor.
            ch = chr(key).upper()
            s = self.text.string
            new_string = s[:self.cursor] + ch + s[self.cursor + 1:] 
            self.text.set_string(new_string)
            self.cursor += 1
        elif key == K_BACKSPACE and self.cursor > 0:
            # Remove the last remove letter and move the cursor back.
            new_string = self.text.string[:-1]
            self.text.set_string(new_string)
            self.cursor -= 1
        elif key == K_RETURN:
            # Submit the value of the input field.
            self.callback(self.text.string)

    def update(self, dt):
        self.blink_timer.update(dt)

    def toggle_blink(self):
        self.cursor_on = not self.cursor_on

    def draw(self, window):
        self.text.draw(window)
        self.draw_cursor(window)

    def draw_cursor(self, window):
        # Assuming a fixed width font so all characters are the same size.
        metrics = self.font.metrics('A')[0]

        pos = self.get_world_position()
        pos = (pos[0] + self.cursor * metrics[1] + 1, pos[1] + self.font.get_ascent() - metrics[3] - 1)
        rect = (pos, (metrics[1] - 2, metrics[3] + 2))
        if self.cursor_on:
            pygame.draw.rect(window, MENU_TEXT_COLOR, rect)

    def get_size(self):
        return self.font.size('   ')
