from json import JSONEncoder


class StatementRequestEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__


class StatementRequestModel(object):

    def __init__(self, file_type, id_request, pv_requester):
        self.file_type = file_type
        self.id_request = id_request
        self.pv_requester = pv_requester
        self.pvs_headquarters = []

    def append_headquarter(self, headquarter):
        self.pvs_headquarters.append(headquarter)
