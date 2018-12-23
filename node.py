class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    #For heap comparisons
    def __lt__(self, otherNode):
        return otherNode.freq > self.freq
