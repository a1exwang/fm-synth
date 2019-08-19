import numpy as np
import scipy.signal
import operators.base
from channels.channel import Channel


class Oscillator(operators.base.Operator):
    """
    Oscillator()

    Input parameters: (f, a, phi)
    f: Frequency
    a: Amplitude
    phi: Phase at time 0
    """

    def __init__(self, input_ops, osc_type='sine', name=None):
        super().__init__(input_ops,
                         1,
                         input_ops[0][0].sr,
                         input_ops[0][0].buffer_size,
                         name)

        self.fns = {
            'sine': lambda f, a, phi, t: a * np.sin(2 * np.pi * f * t + phi),
            'saw': lambda f, a, phi, t: a * scipy.signal.sawtooth(2 * np.pi * f * t + phi, 0),
            'saw_r': lambda f, a, phi, t: a * scipy.signal.sawtooth(2 * np.pi * f * t + phi, 1),
            'triangular': lambda f, a, phi, t: a * scipy.signal.sawtooth(2 * np.pi * f * t + phi, 0.5),
            'square': lambda f, a, phi, t: a * scipy.signal.square(2 * np.pi * f * t + phi),
        }
        self.osc_type = osc_type
        self.osc_id = hash(osc_type) if callable(osc_type) else list(self.fns.keys()).index(osc_type)
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
            get_step=lambda: 1,
            get_range=lambda: (0, len(self.fns)),
        )

    def osc_changed(self, new_osc):
        index = round(new_osc)
        if index >= len(self.fns):
            index = len(self.fns) - 1
        self.osc_id = index
        self.osc_type = list(self.fns.keys())[index]
        self.fn = self.fns[self.osc_type]

    def next_buffer(self, input_buffers, current_count):
        result = np.zeros([self.buffer_size])
        arr_freq, arr_amp, arr_phi = input_buffers
        time_seq = np.array(range(current_count, current_count + self.buffer_size), dtype='float32') / self.sr
        result += self.fn(arr_freq, arr_amp, arr_phi, time_seq)

        return [result]
