import abc

class SNMPCommand(object, metaclass=abc.ABCMeta):

    def __init__(self):
        pass

    def get(self):
        pass

    def set(self):
        pass

    def walk(self):
        pass


class SNMPCommandV1(SNMPCommand):

    def __init__(self):
        pass

    def get(self):
        pass

    def set(self):
        pass

    def walk(self):
        pass


class SNMPCommandV2(SNMPCommandV1):

    def __init__(self):
        pass

    def get(self):
        pass

    def set(self):
        pass

    def walk(self):
        pass

    def bulkget(self):
        pass

    def bulkwalk(self):
        pass
