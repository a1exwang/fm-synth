from operators.base import InputOperator
import numpy as np
from channels.channel import Channel


class ConstOperator(InputOperator):

    def __init__(self, constant, sr=44100, buffer_size=2048, name=None):
        if name is None:
            name = 'Const<%s>#%d' % (constant, self.alloc_id())
        super().__init__(1, sr, buffer_size, name)
        self.constant = constant
        Channel.get_instance().add_channel(name=name,
                                           slot=self.set_val,
                                           get_val=lambda: self.constant,
                                           get_max_values=lambda: 100)

    def set_val(self, val):
        self.constant = val

    def next_buffer(self, input_buffers, n):
        return [np.ones([self.buffer_size], dtype='float32') * self.constant]
