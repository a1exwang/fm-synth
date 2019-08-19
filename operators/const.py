from operators.base import InputOperator
import numpy as np
from channels.channel import Channel


class ConstOperator(InputOperator):

    def __init__(self, constant, sr=44100, buffer_size=2048, name=None, range=(0, 100), step=0.01):
        if name is None:
            name = 'Const<%s>#%d' % (constant, self.alloc_id())
        super().__init__(1, sr, buffer_size, name)
        self.range = range
        self.constant = constant
        Channel.get_instance().add_channel(name=name,
                                           slot=self.set_val,
                                           get_val=lambda: self.constant,
                                           get_range=lambda: range,
                                           get_step=lambda: step)

    def set_val(self, val):
        self.constant = val

    def next_buffer(self, input_buffers, n):
        return [np.ones([self.buffer_size], dtype='float32') * self.constant]
