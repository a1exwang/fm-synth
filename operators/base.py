import numpy as np
from PyQt5.QtCore import QObject, pyqtSlot


class Operator(QObject):
    input_count = 0
    output_count = 0

    def __init__(self, input_ops, in_conn, sr, buffer_size, volume, name):
        super().__init__()
        self.sr = sr
        self.buffer_size = buffer_size
        self.input_ops = input_ops
        self.in_conn = in_conn
        self.output_ops = []
        self.out_conn = []
        self.volume = volume
        self.name = name

        for op in self.input_ops:
            op.add_output_op(self)

    @pyqtSlot(float, name='volume_changed')
    def volume_changed(self, vol):
        if vol <= 0:
            vol = 0
        if vol >= 1:
            vol = 1
        self.volume = vol

    def next_buffer(self, caller, n):
        result = []
        for input_op in self.input_ops:
            val_seq = input_op.next_buffer(self, n)
            result.append(val_seq)

        return result

    def dump(self, operators):
        for op in self.input_ops:
            op.dump(operators)
        op = {
            'ns': 'operators.device_output',
            'type': self.__class__.__name__,
            'name': self.name,
            'input_ops': list(map(lambda x: x.name, self.input_ops)),
            'in_conn': self.in_conn,
            'volume': self.volume,
            'sr': self.sr,
            'buffer_size': self.buffer_size,
        }
        operators.append(op)

    def is_input(self):
        return False

    def get_input_count(self):
        return self.input_count

    def is_output(self):
        return False

    def get_output_count(self):
        return self.output_count

    def add_output_op(self, op):
        self.output_ops.append(op)


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

