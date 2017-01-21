from operators.oscillator import Oscillator
from operators.device_output import DeviceOutput
from operators.midi_input import MIDIInput
from operators.filters import FIRFilter
from oscilloscope import Oscilloscope
from gui import FMSynthGUI
import numpy as np
import functools
import signal

gui = FMSynthGUI()

midi = MIDIInput(sr=44100, buffer_size=2048, bpm=45)
# sine = Oscillator(input_ops=[midi], volume=-1, osc_type='sine')
saw = Oscillator(input_ops=[midi],
                 connection=((0, 0), (0, 1)),
                 volume=1,
                 osc_type='saw',
                 name='Saw')
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
