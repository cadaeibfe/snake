from utility import enum

class Transformable(object):
    '''A base class for objects with a position that can be changed.'''

    def __init__(self, position=(0, 0)):
        '''Initialize the transform at the origin by default.'''
        self.position = position
        self.parent = None

    def set_position(self, position):
        '''Sets a new position.'''
        self.position = position

    def move(self, offset):
        '''Changes the position by an offset.'''
        self.position = (self.position[0] + offset[0],
                         self.position[1] + offset[1])

    def set_parent_transform(self, parent):
        self.parent = parent

    def get_world_position(self):
        '''Returns the position of this object in world coordinates.'''
        position = self.position

        parent = self.parent
        while parent is not None:
            position = (position[0] + parent.position[0],
                        position[1] + parent.position[1])
            parent = parent.parent

        return position



class Text(Transformable):
    '''A class for displaying a text string.'''

    def __init__(self, string, font, color):
        super(Text, self).__init__()
        self.string = string
        self.font = font
        self.color = color
        self.surfaceNeedUpdate = True

    def draw(self, window):
        '''Draws the text to the window.'''
        window.blit(self.get_surface(), self.get_world_position())

    def get_surface(self):
        '''Returns the cached surface, updating it if needed.'''
        if self.surfaceNeedUpdate:
            self.surface = self.font.render(self.string, True, self.color)
            self.surfaceNeedUpdate = False
        return self.surface

    def set_string(self, string):
        '''Sets the text to display a new string.'''
        self.string = string
        self.surfaceNeedUpdate = True

    def get_size(self):
        '''Returns the dimensions of the text surface.'''
        return self.get_surface().get_size()
