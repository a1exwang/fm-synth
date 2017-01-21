from operators.base import InputOperator
import numpy as np


class ConstOperator(InputOperator):

    def __init__(self, constant, sr=44100, buffer_size=2048, volume=1.0, name='ConstOperator'):
        super().__init__(sr, buffer_size, volume, name)
        self.constant = constant

    def next_buffer(self, caller, n):
        return [np.ones([self.buffer_size], dtype='float32') * self.constant]
