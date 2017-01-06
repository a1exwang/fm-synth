import numpy as np


class Operator:

    def __init__(self, input_ops, sr, buffer_size, volume):
        self.sr = sr
        self.buffer_size = buffer_size
        self.input_ops = input_ops
        self.volume = volume

    def next_buffer(self, n):
        result = np.zeros([self.buffer_size])
        for input_op in self.input_ops:
            assert(not input_op.is_input())
            freq_seq = input_op.next_buffer(n)
            result += freq_seq

        return result

    def is_input(self):
        return False

    def is_output(self):
        return False


class InputOperator(Operator):
    def __init__(self, sr, buffer_size, volume):
        super().__init__([], sr, buffer_size, volume)

    def is_input(self):
        return True


class OutputOperator(Operator):
    def __init__(self, input_ops):
        super().__init__(input_ops, input_ops[0].sr, input_ops[0].buffer_size, 1.0)
        self.count = 0

    def is_output(self):
        return True

    def play(self):
        pass
