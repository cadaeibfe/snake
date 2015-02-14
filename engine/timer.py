class Timer(object):
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.elapsed_time = 0

    def update(self, dt):
        self.elapsed_time += dt
        if self.elapsed_time >= self.interval:
            self.elapsed_time -= self.interval
            self.action()
