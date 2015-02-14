import pygame

class ShutterAnimation(object):
    '''A class which animates a top component and a bottom component
    moving towards each other and meeting somewhere in the middle.'''

    def __init__(self, top, bottom, speed, window):
        '''Creates a new animation object with the given top and bottom
        components.'''
        self.top = top
        self.bottom = bottom
        self.speed = speed
        self.pack(window)

    def pack(self, window):
        '''Set the positions of the top and bottom components such
        that they are centered in the window at their final positions.'''
        win_size = window.get_size()
        top_size = self.top.get_size()
        bottom_size = self.bottom.get_size()
        combined_height = top_size[1] + bottom_size[1]

        # Calculate the final positions of the components.
        self.top_final_pos = ((win_size[0] - top_size[0]) / 2,
                              (win_size[1] - combined_height) / 2)

        self.bottom_final_pos = ((win_size[0] - bottom_size[0]) / 2,
                                 self.top_final_pos[1] + top_size[1])

        # Calculate the distance from the component's final position
        # to its initial offscreen position.
        top_distance = self.top_final_pos[1] + top_size[1]
        bottom_distance = win_size[1] - self.bottom_final_pos[1]
        distance = max(top_distance, bottom_distance)

        # Set the components to their initial positions.
        top_initial_y = self.top_final_pos[1] - distance
        bottom_initial_y = self.bottom_final_pos[1] + distance

        self.top.set_position((self.top_final_pos[0], top_initial_y))
        self.bottom.set_position((self.bottom_final_pos[0], bottom_initial_y))

    def update(self, dt):
        '''Updates the shutter animation.'''
        self.top.move((0, self.speed * dt))
        if self.top.position[1] >= self.top_final_pos[1]:
            self.top.set_position(self.top_final_pos)

        self.bottom.move((0, -self.speed * dt))
        if self.bottom.position[1] <= self.bottom_final_pos[1]:
            self.bottom.set_position(self.bottom_final_pos)

    def draw(self, window):
        '''Draws the top and bottom components to the window.'''
        self.top.draw(window)
        self.bottom.draw(window)
