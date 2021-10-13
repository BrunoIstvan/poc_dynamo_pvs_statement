from json import JSONEncoder


class StatementHeadquarterEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__


class StatementHeadquarterModel(object):

    def __init__(self, pv_headquarter):
        self.pv_headquarter = pv_headquarter
        self.pvs = []

    def append_establishments(self, establishments):
        self.pvs = establishments
