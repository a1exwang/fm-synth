import numpy as np
import scipy.signal
import operators.base


class Oscillator(operators.base.Operator):
    input_count = 2
    output_count = 1

    # input_ops: {0: (op1, 0), 1: (op2, 0)}
    def __init__(self, input_ops, in_conn=((0, 0), (0, 1)), volume=1.0,
                 asdr=(0.5, 0.5, 0.5, 0.5), osc_type='sine', name='Osc'):
        super().__init__(input_ops,
                         in_conn,
                         input_ops[0].sr,
                         input_ops[0].buffer_size,
                         volume,
                         name)
        self.osc_type = osc_type
        self.asdr = asdr

        fns = {
            'sine': lambda f, a, t: a * np.sin(2 * np.pi * f * t),
            'saw': lambda f, a, t: a * scipy.signal.sawtooth(2 * np.pi * f * t, 0),
            'saw1': lambda f, a, t: a * scipy.signal.sawtooth(2 * np.pi * f * t, 1),
            'triangular': lambda f, a, t: a * scipy.signal.sawtooth(2 * np.pi * f * t, 0.5),
            'square': lambda f, a, t: a * scipy.signal.square(2 * np.pi * f * t),
        }
        if osc_type in fns:
            self.fn = fns[osc_type]
        elif callable(osc_type):
            self.fn = osc_type
        else:
            raise RuntimeError("Wrong parameter 'osc_type'")

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

        time_seq = np.array(range(current_count, current_count + self.buffer_size), dtype='float32') / self.sr
        result += self.fn(arr_freq, arr_amp, time_seq)

        return [result * self.volume]
