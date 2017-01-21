from operators.base import Operator
import numpy as np


class SumOperator(Operator):

    def __init__(self, input_ops, volume, name='SumOperator'):
        super().__init__(input_ops,
                         ((0, 0),),
                         input_ops[0].sr,
                         input_ops[0].buffer_size,
                         volume,
                         name)

    def next_buffer(self, n):
        outs = super().next_buffer(n)
        result = np.zeros([self.buffer_size])
        for o in outs:
            result += o
        return [result]
