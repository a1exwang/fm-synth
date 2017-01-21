from operators.base import Operator
import numpy as np


class MuxOperator(Operator):

    # mode = 'mux' or 'dup'
    def __init__(self, input_ops, output_count, mode='mux', connections=None, volume=1.0, name='MulOperator'):
        if mode == 'mux':
            conns = []
            assert(output_count == input_ops[0].get_output_count())
            for i in range(output_count):
                conns.append((0, i))
            super().__init__(input_ops,
                             connections if connections else conns,
                             input_ops[0].sr,
                             input_ops[0].buffer_size,
                             volume,
                             name)
        elif mode == 'dup':
            super().__init__(input_ops,
                             tuple([(0, 0)]*output_count),
                             input_ops[0].sr,
                             input_ops[0].buffer_size,
                             volume,
                             name)
        self.mode = mode
        self.output_count = output_count
        self.buffered_data = []
        self.first_buffer_index = 0
        self.n_output_channels = [0]*self.output_count

    def next_buffer(self, caller, n):
        n_buffer_wanted = n // self.buffer_size
        caller_index = self.output_ops.index(caller)
        self.n_output_channels[caller_index] += 1

        i = n_buffer_wanted - self.first_buffer_index
        if i >= len(self.buffered_data):
            outputs = super().next_buffer(self, n)
            self.buffered_data.append(outputs)

        if self.mode == 'mux':
            ret = [self.buffered_data[i][0][caller_index]]
            self.gc()
            return ret
        elif self.mode == 'dup':
            ret = [self.buffered_data[i][0][0]]
            self.gc()
            return ret

    def gc(self):
        min_buffers = min(self.n_output_channels)
        n_gc = min_buffers - self.first_buffer_index
        # delete first +n_gc+ elements
        self.buffered_data = self.buffered_data[n_gc:len(self.buffered_data)-n_gc]
        self.first_buffer_index = min_buffers

    def swap_outputs(self, indexes):
        a = self.output_ops
        self.output_ops = [None] * len(self.output_ops)
        for i, index in enumerate(indexes):
            self.output_ops[i] = a[index]
