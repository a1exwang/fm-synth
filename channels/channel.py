
class Channel:

    """
    A Channel is a tunable parameter driven by any operator or user input.
    """

    instance = None

    def __init__(self):
        self.channels = {}

    @staticmethod
    def get_instance():
        if Channel.instance is None:
            Channel.instance = Channel()
        return Channel.instance

    def add_channel(self, name, slot, get_val,
                    get_max_values=lambda: 100, get_range=lambda: (0, 1), get_step=lambda: 0.01):
        if name in self.channels:
            raise RuntimeError("Duplicate Channel")
        self.channels[name] = {
            'slot': slot,
            'get_val': get_val,
            'get_max': get_max_values,
            'get_range': get_range,
            'get_step': get_step
        }

    def get_channel(self, name):
        return self.channels[name]['slot']

    def get_channel_val(self, name):
        return self.channels[name]['get_val']

    def get_channel_max(self, name):
        return self.channels[name]['get_max']

    def get_channels(self):
        return list(self.channels.keys())

    def get_channel_range_and_step(self, name):
        def _get_rs():
            return [*self.channels[name]['get_range'](), self.channels[name]['get_step']()]
        return _get_rs
