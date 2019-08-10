import numpy as np
import os
from pprint import pprint

from gui.monitors import FMSynthGUI
from operators.const import ConstOperator
from operators.device_output import DeviceOutput
from operators.filters.fir import FIRFilter
from operators.reduce import ReduceOperator
from operators.midi_input import MIDIInput
from operators.oscillator import Oscillator
from oscilloscope import Oscilloscope
import play

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

gui = FMSynthGUI()

sr = 44100
buffer_size = 2048

midi = MIDIInput(gui=gui, sr=sr, buffer_size=buffer_size, bpm=45)

c1_f = ConstOperator(constant=0.5, sr=sr, buffer_size=buffer_size, name='c1_f')
c2_a = ConstOperator(constant=1, sr=sr, buffer_size=buffer_size, name='c2_a')
c3_phi = ConstOperator(constant=0, sr=sr, buffer_size=buffer_size, name='c3_phi')
sine = Oscillator(input_ops=[(c1_f, 0), (c2_a, 0), (c3_phi, 0)], osc_type='sine')

osc100 = Oscilloscope(gui=gui, y_range=(0, 1000), input_ops=[(midi, 0)], name='MIDI Freq')
osc101 = Oscilloscope(gui=gui, y_range=(0, 1), input_ops=[(midi, 1)], name='MIDI Amp')
osc1 = Oscillator(input_ops=[(midi, 0), (midi, 1), (c3_phi, 0)],
                  osc_type='square',
                  name='Osc1')

raw_osc = Oscilloscope(input_ops=[(osc1, 0)], y_range=(0, 1), gui=gui, name='Before-filter Oscilloscope')
filtered = FIRFilter(input_ops=[(osc1, 0)],
                     bands=[(440, 0.7), (440, 880, 1), (880, 1760, 0.9), (1760, 20000, 1)],
                     # window_func=functools.partial(np.kaiser, beta=100),
                     window_func=np.hamming,
                     filter_size=2048,
                     gui=gui,
                     name='Filter1')
osc = Oscilloscope(input_ops=[(filtered, 0)], y_range=(0, 1), gui=gui, name='After-filter Oscilloscope')
out = DeviceOutput(input_op=(filtered, 0), volume=1)

gui.post_init(out)

player = play.Player(sr, buffer_size, (out, 0), [out, osc, raw_osc, osc100, osc101])
player.play_non_blocking()

gui.start()

