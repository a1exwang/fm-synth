from operators.base import OutputOperator
from gui.helpers import LogValueAxis
import numpy as np
import math


class Oscilloscope(OutputOperator):
    name_counter = 0

    def __init__(self, input_ops, x_range=None, x_max=None, x_log=False, y_range=None, y_db=False, gui=None, name=None):
        assert(len(input_ops) == 1)
        super().__init__(input_ops, name=name)
        self.name = name
        self.gui = gui
        self.y_db = y_db
        self.x_log = x_log

        kwargs = {}
        if self.x_log:
            kwargs['axisItems'] = {'bottom': LogValueAxis(orientation='bottom')}

        self.pl = self.gui.add_plot(title=self.name, **kwargs)
        self.y_range = y_range
        self.x_range = x_range
        self.x_max = x_max
        if y_range:
            self.pl.setRange(yRange=self.y_range)
        if x_range:
            if x_log:
                self.pl.setRange(xRange=list(map(math.log, self.x_range)))
            else:
                self.pl.setRange(xRange=self.x_range)
        self.curve = self.pl.plot(pen='y')
        self.ptr = 0

    def next_buffer(self, input_buffers, n):
        input_buffer = input_buffers[0]
        prefilter = np.copy(input_buffer)
        if self.y_db:
            prefilter = 10 * np.log10(input_buffer)
        if self.x_max:
            xs = np.arange(len(input_buffer)) / len(input_buffer) * self.x_max
            if self.x_log:
                xs = np.log(xs)
            args = [xs, prefilter]
        else:
            args = [prefilter]
        self.gui.update_graph_signal.emit(self.curve,
                                          args,
                                          {},
                                          self.pl,
                                          self.ptr == 0)
        self.ptr += 1
        return []
