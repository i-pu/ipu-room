class UserPlugin:

    def __init__(self):
        self.count = 0

    def plus(self):
        self.count += 1
        return {'count': self.count}

    @staticmethod
    def all() -> list:
        return ['plus']

    def __repr__(self):
        return 'count: {}'.format(self.count)
