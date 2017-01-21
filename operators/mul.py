from operators.base import Operator
import numpy as np


class MulOperator(Operator):

    def __init__(self, input_ops, volume=1.0, name='MulOperator'):
        super().__init__(input_ops,
                         ((0, 0),),
                         input_ops[0].sr,
                         input_ops[0].buffer_size,
                         volume,
                         name)

    def next_buffer(self, caller, n):
        outs = super().next_buffer(self, n)
        result = np.ones([self.buffer_size])
        for channels in outs:
            for channel in channels:
                result *= channel
        return [result]

