from engine.timer import Timer

from constants import *
from resourceids import Textures

class Snake(object):
    def __init__(self, map, textures):
        '''Creates a new snake with head at the map's starting point,
        moving right.'''
        x, y = map.get_starting_pos()
        self.segments = [(x - i, y) for i in range(STARTING_LENGTH)]
        self.direction = (1, 0)
        self.direction_buffer = []
        self.eat_callback = None
        self.crash_callback = None
        self.move_timer = Timer(SNAKE_MOVE_INTERVAL, self.move)

        # Keep a reference to the map for collision detection.
        self.map = map

        # Load the image used to draw the snake segments.
        self.spritesheet = textures[Textures.Snake]

    def update(self, dt):
        '''Updates the snake.'''
        self.move_timer.update(dt)

    def move(self):
        '''Moves the snake one unit in the current direction.'''
        # Before moving, change direction if needed.
        while len(self.direction_buffer) > 0:
            # Pop the next direction off the front off the buffer.
            next_direction = self.direction_buffer[0]
            self.direction_buffer.pop(0)

            # Make sure the new direction doesn't cause the snake to
            # double back on itself.
            if (next_direction[0] != -self.direction[0] and
                    next_direction[1] != -self.direction[1]):
                self.direction = next_direction
                break

        new_head = (self.segments[0][0] + self.direction[0],
                    self.segments[0][1] + self.direction[1])
        self.segments.insert(0, new_head)

        # Check if the snake ate the apple.
        if new_head == self.map.apple:
            self.eat_callback()
        else:
            self.segments.pop()

        # Check if the snake crashed into a wall or its own body.
        if (self.map.out_of_bounds(new_head) or
                new_head in self.segments[1:]):
            self.crash_callback()

    def draw(self, window):
        '''Draws the snake.'''
        for i in range(len(self.segments)):
            self.draw_segment(window, i)

    def draw_segment(self, window, i):
        '''Draws the segment at index i to the window.'''
        # Calculate the area of the sprite sheet to blit.
        frame = self.get_frame(i)
        area = (frame * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE)

        # Calculate the position of the segment on screen.
        x = self.segments[i][0] * TILE_SIZE
        y = self.segments[i][1] * TILE_SIZE

        # Blit the image.
        window.blit(self.spritesheet, (x, y), area)

    def get_frame(self, i):
        '''Gets the image frame index for the segment at index i.'''
        if i == 0:
            # The head segment only connects to the next segment.
            return frames[self.get_side(i, i + 1)]
        elif i == len(self.segments) - 1:
            # The tail segment only connects to the previous segment.
            return frames[self.get_side(i, i - 1)]
        else:
            # The rest of the segments have two connections.
            sides = (self.get_side(i, i - 1), self.get_side(i, i + 1))
            return frames[tuple(sorted(sides))]

    def get_side(self, i, j):
        '''Returns which side segment i connects to segment j.'''
        if self.segments[i][0] == self.segments[j][0] - 1:
            return RIGHT
        elif self.segments[i][0] == self.segments[j][0] + 1:
            return LEFT
        elif self.segments[i][1] == self.segments[j][1] - 1:
            return DOWN
        else:
            return UP

# A snake segment can connect on four different sides.
LEFT = 0
RIGHT = 1
DOWN = 2
UP = 3

# Map the side connections to a frame index.
frames = {
        LEFT: 0,
        DOWN: 1,
        RIGHT: 2,
        UP: 3,
        (DOWN, UP): 4,
        (LEFT, RIGHT): 5,
        (RIGHT, UP): 6,
        (RIGHT, DOWN): 7,
        (LEFT, DOWN): 8,
        (LEFT, UP): 9
}
