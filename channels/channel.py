
class Channel:

    instance = None

    def __init__(self):
        self.channels = {}

    @staticmethod
    def get_instance():
        if Channel.instance is None:
            Channel.instance = Channel()
        return Channel.instance

    def add_channel(self, name, slot, get_val):
        if name in self.channels:
            raise RuntimeError("Duplicate Channel")
        self.channels[name] = (slot, get_val)

    def get_channel(self, name):
        return self.channels[name][0]

    def get_channel_val(self, name):
        return self.channels[name][1]

    def get_channels(self):
        return list(self.channels.keys())
