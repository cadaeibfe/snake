from graphics import Transformable

class Container(Transformable):
    '''A class that contains a group of components arranged vertically.'''

    def __init__(self):
        '''Creates an initially empty container.'''
        super(Container, self).__init__()
        self.children = []

    def pack(self, component):
        '''Packs a component into the container.'''
        # Set the position of the new child to be below the bottom
        # of the last child.
        y = 0
        for child in self.children:
            y += child.get_size()[1]
        component.set_position((0, y))

        component.set_parent_transform(self)
        self.children.append(component)

    def align_center(self):
        '''Adjust the x positions of all children to align then
        vertically to the center.'''
        container_width = self.get_size()[0]
        for child in self.children:
            child.set_position(((container_width - child.get_size()[0]) / 2, child.position[1]))

    def update(self, dt):
        print 'updating container...'

    def draw(self, window):
        '''Draws the container's children.'''
        for child in self.children:
            child.draw(window)

    def get_size(self):
        '''Returns the dimensions of this container, calculated by
        adding up the dimensions of the children.'''
        width = 0
        height = 0

        for child in self.children:
            child_size = child.get_size()
            width = max(width, child_size[0])
            height += child_size[1]

        return (width, height)
