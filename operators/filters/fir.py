import numpy as np
from operators.base import Operator
import scipy.signal
import pyqtgraph as pg
import math
from gui.helpers import LogValueAxis


class FIRFilter(Operator):
    input_count = 1
    output_count = 1

    def __init__(self, input_ops, bands, window_func=np.hanning, filter_size=128, gui=None, name=None):
        super().__init__(input_ops,
                         len(input_ops),
                         input_ops[0][0].sr,
                         input_ops[0][0].buffer_size,
                         name)
        self.name = name
        self.gui = gui
        self.filter_size = filter_size
        self.df = float(self.sr) / self.filter_size
        assert(len(input_ops) > 0)
        self.buffer_size = input_ops[0][0].buffer_size
        self.sr = input_ops[0][0].sr
        self.window_func = window_func
        self.window = window_func(filter_size//2)
        self.tw = lambda k: 3.32 * self.sr / k
        self.bands = bands

        # Calculating h(n)
        # f_mid = (f1 + f2) / 2
        # f_c = f2 - f_mid
        #
        # n_1 = np.arange(1, filter_size, dtype='float32')
        # n = np.arange(filter_size, dtype='float32')
        # n_omega_c = 2*np.pi*f_c/self.sr*n_1
        # self.h = np.append([1], np.sin(n_omega_c) / n_omega_c) * self.window * np.cos(n * 2*np.pi*f_mid/self.sr)
        self.h = self.construct_hn(bands)

        self.prev_x = np.zeros([self.filter_size], dtype='float32')

        # Plotting |H(omega)|
        if self.gui is not None:
            self.pl = self.gui.add_plot(self.name + "System function",
                                        axisItems={'bottom': LogValueAxis(orientation='bottom')})
            self.curve = self.pl.plot(pen='y')
            x = (np.arange(len(self.h)//2, dtype='float')+1) * self.sr / len(self.h)
            xx = np.log(x)
            y = 10 * np.log10(np.abs(np.fft.fft(self.h))[:len(self.h)//2] / np.pi)

            self.curve.setData(xx, y)
            self.pl.setLabel('left', "H", units='dB')
            self.pl.setLabel('bottom', "f", units='Hz')
            for band in self.bands:
                if len(band) == 2:
                    freqs = [band[0]]
                else:
                    freqs = [band[0], band[1]]
                for f in freqs:
                    if f > 0:
                        f1_line = pg.InfiniteLine(pos=math.log(f), pen='r', name='f_cut')
                        self.pl.addItem(f1_line)

            self.pl.enableAutoRange('xy', False)

    def construct_hn(self, bands):
        hh = np.zeros([self.filter_size//2], dtype='float32')
        for i, band in enumerate(bands):
            if len(band) == 2 and i == 0:
                # low pass
                f_c, peak = band
                n_1 = np.arange(1, self.filter_size//2, dtype='float32')
                n_omega_c = 2*np.pi*f_c/self.sr*n_1
                hh += peak * np.append([1], np.sin(n_omega_c) / n_omega_c) * self.window

            elif len(band) == 2 and i == len(bands) - 1:
                # high pass
                f_h, peak = band
                f_mid = (f_h + self.sr/2) / 2
                f_c = self.sr/2 - f_mid

                n_1 = np.arange(1, self.filter_size//2, dtype='float32')
                n = np.arange(self.filter_size//2, dtype='float32')
                n_omega_c = 2*np.pi*f_c/self.sr*n_1
                hh += peak * np.append([1], np.sin(n_omega_c) / n_omega_c) * self.window * np.power(-1, n)
            else:
                # band pass
                (f1, f2, peak) = band
                f_mid = (f1 + f2) / 2
                f_c = f2 - f_mid

                n_1 = np.arange(1, self.filter_size//2, dtype='float32')
                n = np.arange(self.filter_size//2, dtype='float32')
                n_omega_c = 2*np.pi*f_c/self.sr*n_1
                h0 = np.append([1], np.sin(n_omega_c) / n_omega_c)
                hh += peak * h0 * self.window * np.cos(n * 2*np.pi*f_mid/self.sr)

        return np.append(hh[::-1], hh)

    def get_tw(self):
        return self.tw(self.filter_size)

    def next_buffer(self, input_buffers, n):
        result = np.zeros([self.buffer_size], dtype='float32')
        xs = input_buffers[0]
        for i in range(self.buffer_size // self.filter_size):
            x_batch = xs[i*self.filter_size:(i+1)*self.filter_size]
            xx = np.append(self.prev_x, x_batch)
            self.prev_x = x_batch

            # This is the original code.
            # yy = np.zeros([2*self.filter_size], dtype='float32')
            # for n in range(2*self.filter_size):
            #     for k in range(np.min([n+1, self.filter_size])):
            #         yy[n] += xx[n - k] * self.h[k]
            # y_batch = yy[self.filter_size:2*self.filter_size]
            # Here's optimized version:
            start = self.filter_size / 2 + 1
            # TODO: Why does this need division by PI?
            start_i = int(start)
            conv = scipy.signal.fftconvolve(xx, self.h, mode='same')
            y_batch = conv[start_i:start_i+self.filter_size] / np.pi

            result[i*self.filter_size:(i+1)*self.filter_size] = y_batch
        return [result]

