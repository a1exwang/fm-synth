from operators.base import Operator
import numpy as np


class Oscilloscope(Operator):
    input_count = 1
    output_count = 1

    def __init__(self, input_ops, connections=((0, 0),), gui=None, name='Oscilloscope'):
        super().__init__(input_ops, connections, input_ops[0].sr, input_ops[0].buffer_size, 1.0, name)
        self.name = name
        self.gui = gui

        self.pl = self.gui.add_plot(title=self.name)
        self.pl.setRange(yRange=[-1, 1])
        self.curve = self.pl.plot(pen='y')
        self.ptr = 0

    def next_buffer(self, caller, n):
        result = super().next_buffer(self, n)
        i_op, i_channel = self.in_conn[0]
        self.gui.update_graph_signal.emit(self.curve,
                                          np.copy(result[i_op][i_channel]),
                                          self.pl,
                                          self.ptr == 0)
        self.ptr += 1
        return [result[i_op][i_channel]]
