import numpy as np
import os
from pprint import pprint

from gui.monitors import FMSynthGUI
from operators.const import ConstOperator
from operators.device_output import DeviceOutput
from operators.filters.fir import FIRFilter
from operators.mux import MuxOperator
from operators.mul import MulOperator
from operators.midi_input import MIDIInput
from operators.oscillator import Oscillator
from oscilloscope import Oscilloscope

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

gui = FMSynthGUI()

sr = 44100
buffer_size = 2048

midi = MIDIInput(gui=gui, sr=sr, buffer_size=buffer_size, bpm=45)

mux = MuxOperator(input_ops=[midi], output_count=2)

c1_f = ConstOperator(constant=0.5, sr=sr, buffer_size=buffer_size, name='c1_f')
c2_a = ConstOperator(constant=1, sr=sr, buffer_size=buffer_size, name='c2_a')
c3_phi = ConstOperator(constant=0, sr=sr, buffer_size=buffer_size, name='c3_phi')
sine = Oscillator(input_ops=[c1_f, c2_a, c3_phi], osc_type='sine')

mul = MulOperator(input_ops=[c2_a, mux])

osc100 = Oscilloscope(gui=gui, input_ops=[mul], connections=((0, 0),), name='MIDI Osc')
osc1 = Oscillator(input_ops=[mux, osc100, c3_phi],
                  volume=1,
                  osc_type='square',
                  name='Osc1')

mux.swap_outputs((1, 0))
raw_osc = Oscilloscope(input_ops=[osc1], gui=gui, name='Before-filter Oscilloscope')
filtered = FIRFilter(input_ops=[raw_osc],
                     bands=[(440, 0.7), (440, 880, 1), (880, 1760, 0.9), (1760, 20000, 1)],
                     # window_func=functools.partial(np.kaiser, beta=100),
                     window_func=np.hamming,
                     filter_size=2048,
                     gui=gui,
                     name='Filter1')
osc = Oscilloscope(input_ops=[filtered], gui=gui, name='After-filter Oscilloscope')
out = DeviceOutput(input_op=osc, volume=1)

gui.post_init(out)

# out.play()
out.play_non_blocking()
gui.start()

