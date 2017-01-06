from operators.oscillator import Oscillator
from operators.device_output import DeviceOutput
from operators.midi_input import MIDIInput
from operators.filters import BandPassFilter
from oscilloscope import Oscilloscope
from gui import FMSynthGUI
import numpy as np
import functools

gui = FMSynthGUI()

midi = MIDIInput(sr=44100, buffer_size=2048, bpm=45)
# sine = Oscillator(input_ops=[midi], volume=-1, osc_type='sine')
saw = Oscillator(input_ops=[midi], volume=-0.7, osc_type='saw')
raw_osc = Oscilloscope(input_ops=[saw], gui=gui, name='Before-filter Oscilloscope')
filtered = BandPassFilter(input_ops=[raw_osc],
                          bands=[(440, 0.5), (440, 880, 1), (880, 1760, 0), (1760, 3520, 1)],
                          # window_func=functools.partial(np.kaiser, beta=100),
                          window_func=np.hamming,
                          filter_size=2048, gui=gui)
osc = Oscilloscope(input_ops=[filtered], gui=gui, name='After-filter Oscilloscope')
out = DeviceOutput(input_ops=[osc], volume=1)

# out.play()
out.play_non_blocking()
gui.start()
