import numpy as np


class Operator:
    input_count = 0
    output_count = 0

    def __init__(self, input_ops, connection, sr, buffer_size, volume, name):
        self.sr = sr
        self.buffer_size = buffer_size
        self.input_ops = input_ops
        self.connections = connection
        self.volume = volume
        self.name = name

    def next_buffer(self, n):
        result = []
        for input_op in self.input_ops:
            assert(not input_op.is_input())
            val_seq = input_op.next_buffer(n)
            result += val_seq

        return result

    def is_input(self):
        return False

    def get_input_count(self):
        return self.input_count

    def is_output(self):
        return False

    def get_output_count(self):
        return self.output_count


class InputOperator(Operator):
    input_count = 0

    def __init__(self, sr, buffer_size, volume, name='InputOperator'):
        super().__init__([], ((0, 0),), sr, buffer_size, volume, name)

    def is_input(self):
        return True


class OutputOperator(Operator):
    output_count = 0

    def __init__(self, input_ops, volume=1.0, name='OutputOperator'):
        super().__init__(input_ops, ((0, 0),), input_ops[0].sr, input_ops[0].buffer_size, volume, name)
        self.count = 0

    def is_output(self):
        return True

    def play(self):
        pass

