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
range_1 = (-1, 1)

canon1 = [
    {'note': 'C5', 'onoff': True, 'velocity': 1, 't': 0.1},
    {'note': 'C5', 'onoff': False, 'velocity': 1, 't': 1.1},
    {'note': 'G4', 'onoff': True, 'velocity': 1, 't': 1.1},
    {'note': 'G4', 'onoff': False, 'velocity': 1, 't': 2.1},
    {'note': 'A4', 'onoff': True, 'velocity': 1, 't': 2.1},
    {'note': 'A4', 'onoff': False, 'velocity': 1, 't': 3.1},
    {'note': 'E4', 'onoff': True, 'velocity': 1, 't': 3.1},
    {'note': 'E4', 'onoff': False, 'velocity': 1, 't': 4.1},
    {'note': 'F4', 'onoff': True, 'velocity': 1, 't': 4.1},
    {'note': 'F4', 'onoff': False, 'velocity': 1, 't': 5.1},
    {'note': 'C4', 'onoff': True, 'velocity': 1, 't': 5.1},
    {'note': 'C4', 'onoff': False, 'velocity': 1, 't': 6.1},
    {'note': 'F4', 'onoff': True, 'velocity': 1, 't': 6.1},
    {'note': 'F4', 'onoff': False, 'velocity': 1, 't': 7.1},
    {'note': 'G4', 'onoff': True, 'velocity': 1, 't': 7.1},
    {'note': 'G4', 'onoff': False, 'velocity': 1, 't': 8.1},
]

canon2 = [
    {'note': 'C5', 'onoff': True, 'velocity': 1, 't': 0.1},
    {'note': 'C5', 'onoff': False, 'velocity': 1, 't': 1.1},
    {'note': 'G4', 'onoff': True, 'velocity': 1, 't': 1.1},
    {'note': 'G4', 'onoff': False, 'velocity': 1, 't': 2.1},
    {'note': 'A4', 'onoff': True, 'velocity': 1, 't': 2.1},
    {'note': 'A4', 'onoff': False, 'velocity': 1, 't': 3.1},
    {'note': 'E4', 'onoff': True, 'velocity': 1, 't': 3.1},
    {'note': 'E4', 'onoff': False, 'velocity': 1, 't': 4.1},
    {'note': 'F4', 'onoff': True, 'velocity': 1, 't': 4.1},
    {'note': 'F4', 'onoff': False, 'velocity': 1, 't': 5.1},
    {'note': 'C4', 'onoff': True, 'velocity': 1, 't': 5.1},
    {'note': 'C4', 'onoff': False, 'velocity': 1, 't': 6.1},
    {'note': 'F4', 'onoff': True, 'velocity': 1, 't': 6.1},
    {'note': 'F4', 'onoff': False, 'velocity': 1, 't': 7.1},
    {'note': 'G4', 'onoff': True, 'velocity': 1, 't': 7.1},
    {'note': 'G4', 'onoff': False, 'velocity': 1, 't': 8.1},
]

canon3 = [
    {'note': 'C5', 'onoff': True, 'velocity': 1, 't': 0.1},
    {'note': 'C5', 'onoff': False, 'velocity': 1, 't': 1.1},
    {'note': 'G4', 'onoff': True, 'velocity': 1, 't': 1.1},
    {'note': 'G4', 'onoff': False, 'velocity': 1, 't': 2.1},
    {'note': 'A4', 'onoff': True, 'velocity': 1, 't': 2.1},
    {'note': 'A4', 'onoff': False, 'velocity': 1, 't': 3.1},
    {'note': 'E4', 'onoff': True, 'velocity': 1, 't': 3.1},
    {'note': 'E4', 'onoff': False, 'velocity': 1, 't': 4.1},
    {'note': 'F4', 'onoff': True, 'velocity': 1, 't': 4.1},
    {'note': 'F4', 'onoff': False, 'velocity': 1, 't': 5.1},
    {'note': 'C4', 'onoff': True, 'velocity': 1, 't': 5.1},
    {'note': 'C4', 'onoff': False, 'velocity': 1, 't': 6.1},
    {'note': 'F4', 'onoff': True, 'velocity': 1, 't': 6.1},
    {'note': 'F4', 'onoff': False, 'velocity': 1, 't': 7.1},
    {'note': 'G4', 'onoff': True, 'velocity': 1, 't': 7.1},
    {'note': 'G4', 'onoff': False, 'velocity': 1, 't': 8.1},
]

midi = MIDIInput(gui=gui, sr=sr, buffer_size=buffer_size, bpm=45)
scope100 = Oscilloscope(gui=gui, y_range=(0, 1000), input_ops=[(midi, 0)], name='MIDI Freq')
scope101 = Oscilloscope(gui=gui, y_range=range_1, input_ops=[(midi, 1)], name='MIDI Amp')

one = ConstOperator(constant=1, sr=sr, buffer_size=buffer_size, name='c2_a')
half = ConstOperator(constant=0.5, sr=sr, buffer_size=buffer_size, name='0.5')
zero = ConstOperator(constant=0, sr=sr, buffer_size=buffer_size, name='c3_phi')

sine_lfo = Oscillator(
    input_ops=[
        (ConstOperator(constant=3, sr=sr, buffer_size=buffer_size), 0),
        (ConstOperator(constant=0.3, sr=sr, buffer_size=buffer_size), 0),
        (zero, 0)],
    osc_type='sine')
sine_lfo_scope = Oscilloscope(input_ops=[(sine_lfo, 0)], y_range=range_1, gui=gui, name='LFO')

osc1 = Oscillator(input_ops=[(midi, 0), (midi, 1), (zero, 0)],
                  osc_type='sine',
                  name='Osc1')
osc1_scope = Oscilloscope(input_ops=[(osc1, 0)], y_range=range_1, gui=gui, name='Osc1 Out')

osc2 = Oscillator(input_ops=[(osc1, 0), (midi, 1), (zero, 0)],
                  osc_type='square',
                  name='Osc2')
osc2_scope = Oscilloscope(input_ops=[(osc2, 0)], y_range=range_1, gui=gui, name='Osc2 Out')

lfo = ReduceOperator(
    input_ops=[(osc1, 0), (sine_lfo, 0)], operation=ReduceOperator.ReduceOperations.MUL, name='LFO out')

scope_before = Oscilloscope(input_ops=[(lfo, 0)], y_range=range_1, gui=gui, name='Before-filter Oscilloscope')
filtered = FIRFilter(input_ops=[(lfo, 0)],
                     bands=[(440, 0.7), (440, 880, 1), (880, 1760, 0.9), (1760, 20000, 1)],
                     # window_func=functools.partial(np.kaiser, beta=100),
                     window_func=np.hamming,
                     filter_size=2048,
                     gui=gui,
                     name='Filter1')
scope_after = Oscilloscope(input_ops=[(filtered, 0)], y_range=range_1, gui=gui, name='After-filter Oscilloscope')
out = DeviceOutput(input_op=(filtered, 0), volume=1)

gui.post_init(out)

player = play.Player(sr, buffer_size, (out, 0), [out, scope100, scope101, scope_before, scope_after, sine_lfo_scope,
                                                 osc1_scope, osc2_scope])
player.play_non_blocking()

gui.start()

