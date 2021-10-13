class PvModel(object):

    def __init__(self, pv_code, pv_name, active):
        self.__pv_code = pv_code
        self.__pv_name = pv_name
        self.__active = active

    @property
    def code(self):
        return self.__pv_code

    @property
    def name(self):
        return self.__pv_name

    @property
    def active(self):
        return self.__active
