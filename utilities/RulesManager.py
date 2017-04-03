class Rule(object):

    def __init__(self, device, state, time, repeat):
        self.device = device
        self.state = state
        self.time = time
        self.repeat = repeat

    def __cmp__(self, other):
        return cmp(self.time, other.time)