class Piece (object):
    def __init__(self):
        super().__init__()
        self.origin = False
        self.offset = 0
        self.length = 0

class State(object):
    def __init__(self):
        super().__init__()
        self.pieces = []

