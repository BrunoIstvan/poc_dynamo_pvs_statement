class PvsStatementModel(object):

    def __init__(self, file_type, pv_establishment, pv_headquarter, pv_requester, id_request, active):
        self.__active = active
        self.__file_type = file_type
        self.__id_request = id_request
        self.__pv_establishment = pv_establishment
        self.__pv_headquarter = pv_headquarter
        self.__pv_requester = pv_requester

    @property
    def active(self):
        return self.__active

    @property
    def file_type(self):
        return self.__file_type

    @property
    def id_request(self):
        return self.__id_request

    @property
    def pv_establishment(self):
        return self.__pv_establishment

    @property
    def pv_headquarter(self):
        return self.__pv_headquarter

    @property
    def pv_requester(self):
        return self.__pv_requester

    @staticmethod
    def get_data(data):
        result = list()
        for d in data:
            result.append(PvsStatementModel.parse(item=d))

        return result

    @staticmethod
    def parse(item):
        return PvsStatementModel(
            file_type=item['fileType'],
            pv_establishment=item['pvEstablishment'],
            pv_headquarter=item['pvHeadquarter'],
            pv_requester=item['pvRequester'],
            id_request=int(item['idRequest']),
            active=item['active']
        )
