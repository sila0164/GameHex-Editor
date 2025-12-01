
class IdDict:
    def __init__(self, dictionary):
        self.name = dictionary
        self.id = {v: k for k, v in dictionary.items()}
