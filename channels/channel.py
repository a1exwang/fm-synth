
class Channel:

    instance = None

    def __init__(self):
        self.channels = {}

    @staticmethod
    def get_instance():
        if Channel.instance is None:
            Channel.instance = Channel()
        return Channel.instance

    def add_channel(self, name, slot, get_val, get_max_values=lambda: 100):
        if name in self.channels:
            raise RuntimeError("Duplicate Channel")
        self.channels[name] = {'slot': slot, 'get_val': get_val, 'get_max': get_max_values}

    def get_channel(self, name):
        return self.channels[name]['slot']

    def get_channel_val(self, name):
        return self.channels[name]['get_val']

    def get_channel_max(self, name):
        return self.channels[name]['get_max']

    def get_channels(self):
        return list(self.channels.keys())
