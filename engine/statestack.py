class PendingChange(object):
    def __init__(self, action, stateID=None, args=None):
        self.action = action
        self.stateID = stateID
        self.args = args

# Pending change actions.
Push = 0
Pop = 1
Clear = 2

class StateStack(object):
    def __init__(self, window):
        self.stack = []
        self.pending_changes = []
        self.factories = {}
        self.window = window

    def handle_event(self, event):
        '''Passes an event to the active states, from top to bottom.
        Stop if a state's handle_event() method returns false.'''
        for state in reversed(self.stack):
            if not state.handle_event(event):
                break

        self.apply_pending_changes()

    def update(self, dt):
        '''Updates the active states, from top to bottom. Stop if
        a state's update() method returns false.'''
        for state in reversed(self.stack):
            if not state.update(dt):
                break

        self.apply_pending_changes()

    def draw(self):
        '''Renders all active states from bottom to top.'''
        for state in self.stack:
            state.draw()

    def register_state(self, stateID, state_class):
        '''Registers a state class to be associated with an ID.'''
        self.factories[stateID] = state_class

    def push_state(self, stateID, *args):
        '''Queues a new state to be pushed onto the top of the stack.'''
        self.pending_changes.append(PendingChange(Push, stateID, args))

    def pop_state(self):
        '''Queues the top state to be removed.'''
        self.pending_changes.append(PendingChange(Pop))

    def clear_states(self):
        '''Queues all states in the stack to be removed.'''
        self.pending_changes.append(PendingChange(Clear))

    def is_empty(self):
        '''Returns true if the stack contains no states.'''
        return len(self.stack) == 0

    def apply_pending_changes(self):
        '''Performs queued stack operations.'''
        for change in self.pending_changes:
            if change.action == Push:
                state = self.create_state(change.stateID, change.args)
                self.stack.append(state)
            elif change.action == Pop:
                self.stack.pop()
            elif change.action == Clear:
                self.stack = []

        self.pending_changes = []

    def create_state(self, stateID, args):
        '''Instantiates the state with the given ID.'''
        return self.factories[stateID](self, self.window, args)
