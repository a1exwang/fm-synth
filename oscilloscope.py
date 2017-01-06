from operators.base import Operator
import numpy as np


class Oscilloscope(Operator):
    def __init__(self, input_ops, gui=None, name='Oscilloscope'):
        super().__init__(input_ops, input_ops[0].sr, input_ops[0].buffer_size, 1.0)
        self.name = name
        self.gui = gui

        self.pl = self.gui.add_plot(title=name)
        self.pl.setRange(yRange=[-1, 1])
        self.curve = self.pl.plot(pen='y')
        self.ptr = 0

    def next_buffer(self, n):
        result = super().next_buffer(n)
        self.curve.setData(result)
        if self.ptr == 0:
            self.pl.enableAutoRange('x', False)
        self.ptr += 1
        return result
