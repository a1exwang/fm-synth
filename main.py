import numpy as np

from gui import FMSynthGUI
from operators.const import ConstOperator
from operators.device_output import DeviceOutput
from operators.filters.fir import FIRFilter
from operators.mux import MuxOperator
from operators.mul import MulOperator
from operators.midi_input import MIDIInput
from operators.oscillator import Oscillator
from oscilloscope import Oscilloscope

gui = FMSynthGUI()

sr = 44100
buffer_size = 2048

midi = MIDIInput(sr=sr, buffer_size=buffer_size, bpm=45)

mux = MuxOperator(input_ops=[midi], output_count=2)

c1 = ConstOperator(constant=0.5, sr=sr, buffer_size=buffer_size)
c2 = ConstOperator(constant=1, sr=sr, buffer_size=buffer_size)
sine = Oscillator(input_ops=[c1, c2], in_conn=((0, 0), (1, 0)), osc_type='sine')

mul = MulOperator(input_ops=[sine, mux])

saw = Oscillator(input_ops=[mux, mul],
                 in_conn=((0, 0), (1, 0)),
                 volume=1,
                 osc_type='saw',
                 name='Saw')

mux.swap_outputs((1, 0))
raw_osc = Oscilloscope(input_ops=[saw], gui=gui, name='Before-filter Oscilloscope')
filtered = FIRFilter(input_ops=[raw_osc],
                     bands=[(440, 0.7), (440, 880, 1), (880, 1760, 0.9), (1760, 20000, 1)],
                     # window_func=functools.partial(np.kaiser, beta=100),
                     window_func=np.hamming,
                     filter_size=2048,
                     gui=gui,
                     name='Filter1')
osc = Oscilloscope(input_ops=[filtered], gui=gui, name='After-filter Oscilloscope')
out = DeviceOutput(input_op=osc, volume=1)

# out.play()
out.play_non_blocking()
gui.start()
