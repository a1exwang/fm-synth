from PyQt5.QtCore import QObject


class Operator(QObject):
    def __init__(self, input_ops, output_count, sr, buffer_size, name):
        super().__init__()
        self.sr = sr
        self.buffer_size = buffer_size
        self.out_conn = []
        self.name = name
        self.output_count = output_count
        self.current_offset = 0
        self.output_buffers = []
        self.input_ops = input_ops
        for input_op, channel in self.input_ops:
            assert channel < input_op.output_count, \
                "Cannot connect the '%s'(%s).output[%d] to '%s'(%s). It has only %d outputs. Index %d is out of bounds" % \
                (type(input_op), input_op.name, channel, type(self), self.name, input_op.output_count, channel,)

    def next_buffer(self, input_buffers, n):
        return []

    def dump(self, operators):
        for op in self.input_ops:
            op[0].dump(operators)
        op = {
            'ns': 'operators.device_output',
            'type': self.__class__.__name__,
            'name': self.name,
            'input_ops': list(map(lambda x: x[0].name, self.input_ops)),
            'output_count': self.output_count,
            'sr': self.sr,
            'buffer_size': self.buffer_size,
        }
        operators.append(op)

    def get_input_count(self):
        return len(self.input_ops)

    def get_output_count(self):
        return self.output_count

    def is_input(self):
        return self.get_input_count() == 0

    def is_output(self):
        return self.get_output_count() == 0

    def step(self, current_offset):
        for i in range(current_offset - self.current_offset):
            input_buffers = []
            for op, channel in self.input_ops:
                op.step(current_offset)
                input_buffers.append(op.output_buffers[channel])
            self.output_buffers = self.next_buffer(input_buffers, self.current_offset * self.buffer_size)
            if not self.is_output():
                assert(len(self.output_buffers) == self.output_count)
            self.current_offset += 1


class InputOperator(Operator):
    def __init__(self, output_count, sr, buffer_size, name='InputOperator'):
        super().__init__([], output_count, sr, buffer_size, name)


class OutputOperator(Operator):
    def __init__(self, input_ops, name='OutputOperator'):
        super().__init__(input_ops, 0, input_ops[0][0].sr, input_ops[0][0].buffer_size, name)

