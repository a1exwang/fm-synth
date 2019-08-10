from operators.base import OutputOperator
import numpy as np


class Oscilloscope(OutputOperator):
    def __init__(self, input_ops, y_range=None, gui=None, name='Oscilloscope'):
        assert(len(input_ops) == 1)

        super().__init__(input_ops, name=name)
        self.name = name
        self.gui = gui

        self.pl = self.gui.add_plot(title=self.name)
        self.y_range = y_range
        if y_range:
            self.pl.setRange(yRange=self.y_range)
        self.curve = self.pl.plot(pen='y')
        self.ptr = 0

    def next_buffer(self, input_buffers, n):
        input_buffer = input_buffers[0]
        self.gui.update_graph_signal.emit(self.curve,
                                          np.copy(input_buffer),
                                          self.pl,
                                          self.ptr == 0)
        self.ptr += 1
        return []
