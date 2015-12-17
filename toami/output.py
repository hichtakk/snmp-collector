import abc


class BaseOutput(object, metaclass=abc.ABCMeta):

    def __init__(self, args):
        self._args = args

    @abc.abstractmethod
    def print(self):
        raise NotImplementedError()


class DefaultOutput(BaseOutput):

    def print(self, results):
        for result in results:
            if self._args.pruning and result['type'] == 'NoSuchInstance':
                continue
            host = result['address'] if self._args.number else result['host']
            print('{0}\t{1}\t{2}\t{3}\t{4}'.format(host, result['label'],
                                                   result['oid'],
                                                   result['type'],
                                                   result['value']))

class SensuOutput(BaseOutput):

    def print(self, results):
        for result in results:
            if self._args.pruning and result['type'] == 'NoSuchInstance':
                continue
            print('{0}.{1} {2} {3}'.format(result['host'], result['label'],
                                           result['value'], result['time']))


def getPrinter(args):
    if args.sensu:
        return SensuOutput(args)
    else:
        return DefaultOutput(args)
