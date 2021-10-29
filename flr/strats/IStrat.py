from ..broker.IBroker import IBroker

class IStrat:
    def __init__(self, broker: IBroker):
        self.broker = broker

    def loop(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
