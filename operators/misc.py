import numpy as np
import operators.base


class Limiter(operators.base.Operator):
    """
    """

    def __init__(self, input_ops, min_value=-1.0, max_value=1.0, name=None):
        super().__init__(input_ops,
                         len(input_ops),
                         input_ops[0][0].sr,
                         input_ops[0][0].buffer_size,
                         name)
        self.min_value = min_value
        self.max_value = max_value

    def next_buffer(self, input_buffers, current_count):
        ret = []
        for input_buffer in input_buffers:
            ret.append(np.clip(input_buffer, self.min_value, self.max_value))
        return ret
