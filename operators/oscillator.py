import numpy as np
import scipy.signal
import operators.base


class Oscillator(operators.base.Operator):
    def __init__(self, input_ops, volume=1.0, osc_type='sine'):
        super().__init__(input_ops,
                         input_ops[0].sr,
                         input_ops[0].buffer_size,
                         volume)
        self.osc_type = osc_type

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

    def next_buffer(self, current_count):

        result = np.zeros([self.buffer_size])
        for input_op in self.input_ops:
            if input_op.is_input():
                freq_seq, amp_seq = input_op.next_buffer(current_count)
                indexes = np.array(range(current_count, current_count + self.buffer_size), dtype='float32')
                t_seq = indexes / self.sr
                result += self.fn(freq_seq, amp_seq, t_seq)
            else:
                freq_seq = input_op.next_buffer(current_count)
                indexes = np.array(range(current_count, current_count + self.buffer_size), dtype='float32')
                t_seq = indexes / self.sr
                result += self.fn(freq_seq, 1, t_seq)

        return result * self.volume
