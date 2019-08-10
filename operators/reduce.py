from operators.base import Operator
import numpy as np
import enum


class ReduceOperator(Operator):

    """
    Input n
    Output 1

    Input 0 * Input 1 * Input 2 ...
    """

    class ReduceOperations(enum.Enum):
        # name, initial value, reduce function
        SUM = ('sum', 0, lambda a, b: a + b)
        MUL = ('mul', 1, lambda a, b: a * b)

    def __init__(self, input_ops, operation, name=None):
        if name is None:
            name = "ReduceOperator<%s>" % (operation[0],)
        super().__init__(input_ops,
                         1,
                         input_ops[0].sr,
                         input_ops[0].buffer_size,
                         name)
        self.operation = operation

    def next_buffer(self, input_buffers, n):
        result = np.ones([self.buffer_size]) * self.operation[1]
        for input_buffer in input_buffers:
            result = self.operation[2](result, input_buffer)
        return [result]

