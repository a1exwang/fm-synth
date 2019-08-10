import numpy as np
import scipy.signal
import operators.base
from channels.channel import Channel


class Oscillator(operators.base.Operator):
    input_count = 2
    output_count = 1

    # input_ops: {0: (op1, 0), 1: (op2, 0)}
    def __init__(self, input_ops, in_conn=((0, 0), (1, 0), (2, 0)), volume=1.0,
                 asdr=(0.5, 0.5, 0.5, 0.5), osc_type='sine', name='Osc'):
        """
         Oscillator()
         @in_conn: An list of tuples, one of which is (osc_index, channel_index).
           if in_conn[i] is (osc_index, channel_index), it means for input operator `osc_index`,
           connect its output channel `channel_index` to parameter `i`.
        """
        super().__init__(input_ops,
                         in_conn,
                         input_ops[0].sr,
                         input_ops[0].buffer_size,
                         volume,
                         name)
        self.asdr = asdr

        self.fns = {
            'sine': lambda f, a, phi, t: a * np.sin(2 * np.pi * f * t + phi),
            'saw': lambda f, a, phi, t: a * scipy.signal.sawtooth(2 * np.pi * f * t + phi, 0),
            'saw_r': lambda f, a, phi, t: a * scipy.signal.sawtooth(2 * np.pi * f * t + phi, 1),
            'triangular': lambda f, a, phi, t: a * scipy.signal.sawtooth(2 * np.pi * f * t + phi, 0.5),
            'square': lambda f, a, phi, t: a * scipy.signal.square(2 * np.pi * f * t + phi),
        }
        self.osc_type = osc_type
        self.osc_id = list(self.fns.keys()).index(osc_type)
        if osc_type in self.fns:
            self.fn = self.fns[osc_type]
        elif callable(osc_type):
            self.fn = osc_type
        else:
            raise RuntimeError("Wrong parameter 'osc_type', either an oscillator name or a callable")

        Channel.get_instance().add_channel(
            name='Osc<%s,%s>::wavelet' % (self.osc_type if type(self.osc_type) is str else 'custom', self.name),
            slot=self.osc_changed,
            get_val=lambda: self.osc_id,
            get_max_values=lambda: len(self.fns),
        )

    def osc_changed(self, new_osc):
        index = round(new_osc * len(self.fns))
        if index >= len(self.fns):
            index = len(self.fns) - 1
        self.osc_id = index
        self.osc_type = list(self.fns.keys())[index]
        self.fn = self.fns[self.osc_type]

    def is_input(self):
        return False

    def next_buffer(self, caller, current_count):
        result = np.zeros([self.buffer_size])
        op_outs = []
        for input_op in self.input_ops:
            # if input_op.is_input():
            outs = input_op.next_buffer(self, current_count)
            op_outs.append(outs)

        freq_op, freq_channel = self.in_conn[0]
        arr_freq = op_outs[freq_op][freq_channel]

        amp_op, amp_channel = self.in_conn[1]
        arr_amp = op_outs[amp_op][amp_channel]

        phi_op, phi_channel = self.in_conn[2]
        arr_phi = op_outs[phi_op][phi_channel]

        time_seq = np.array(range(current_count, current_count + self.buffer_size), dtype='float32') / self.sr
        result += self.fn(arr_freq, arr_amp, arr_phi, time_seq)

        return [result * self.volume]
