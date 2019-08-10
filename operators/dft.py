import numpy as np
import operators.base


class DFT(operators.base.Operator):
    """
    """

    def __init__(self, input_ops, name=None):
        super().__init__(input_ops,
                         len(input_ops),
                         input_ops[0][0].sr,
                         input_ops[0][0].buffer_size,
                         name)

    def get_cut_frequency(self):
        return self.sr / 2

    def next_buffer(self, input_buffers, current_count):
        ret = []
        for input_buffer in input_buffers:
            val = np.abs(np.fft.rfft(input_buffer)) / (len(input_buffer) / 2)
            ret.append(val)
        return ret
