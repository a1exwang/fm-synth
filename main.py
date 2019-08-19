import numpy as np
import os
import numbers
from pprint import pprint

from gui.monitors import FMSynthGUI
from operators.const import ConstOperator
from operators.base import Operator
from operators.device_output import DeviceOutput
from operators.filters.fir import FIRFilter
from operators.reduce import ReduceOperator
from operators.midi_input import MIDIInput
from operators.oscillator import Oscillator
from operators.dft import DFT
from operators.misc import Limiter
from oscilloscope import Oscilloscope
import play

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

gui = FMSynthGUI()

sr = 44100
buffer_size = 2048
range_1 = (-1, 1)

canon_bass = [
    {'note': 'C4', 'onoff': True, 'velocity': 1, 't': 0.1},
    {'note': 'C4', 'onoff': False, 'velocity': 1, 't': 1.1},
    {'note': 'G3', 'onoff': True, 'velocity': 1, 't': 1.1},
    {'note': 'G3', 'onoff': False, 'velocity': 1, 't': 2.1},
    {'note': 'A3', 'onoff': True, 'velocity': 1, 't': 2.1},
    {'note': 'A3', 'onoff': False, 'velocity': 1, 't': 3.1},
    {'note': 'E3', 'onoff': True, 'velocity': 1, 't': 3.1},
    {'note': 'E3', 'onoff': False, 'velocity': 1, 't': 4.1},
    {'note': 'F3', 'onoff': True, 'velocity': 1, 't': 4.1},
    {'note': 'F3', 'onoff': False, 'velocity': 1, 't': 5.1},
    {'note': 'C3', 'onoff': True, 'velocity': 1, 't': 5.1},
    {'note': 'C3', 'onoff': False, 'velocity': 1, 't': 6.1},
    {'note': 'F3', 'onoff': True, 'velocity': 1, 't': 6.1},
    {'note': 'F3', 'onoff': False, 'velocity': 1, 't': 7.1},
    {'note': 'G3', 'onoff': True, 'velocity': 1, 't': 7.1},
    {'note': 'G3', 'onoff': False, 'velocity': 1, 't': 8.1},
]

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
    {'note': 'E5', 'onoff': True, 'velocity': 1, 't': 0.1},
    {'note': 'E5', 'onoff': False, 'velocity': 1, 't': 1.1},
    {'note': 'B4', 'onoff': True, 'velocity': 1, 't': 1.1},
    {'note': 'B4', 'onoff': False, 'velocity': 1, 't': 2.1},
    {'note': 'C5', 'onoff': True, 'velocity': 1, 't': 2.1},
    {'note': 'C5', 'onoff': False, 'velocity': 1, 't': 3.1},
    {'note': 'G4', 'onoff': True, 'velocity': 1, 't': 3.1},
    {'note': 'G4', 'onoff': False, 'velocity': 1, 't': 4.1},
    {'note': 'A4', 'onoff': True, 'velocity': 1, 't': 4.1},
    {'note': 'A4', 'onoff': False, 'velocity': 1, 't': 5.1},
    {'note': 'E4', 'onoff': True, 'velocity': 1, 't': 5.1},
    {'note': 'E4', 'onoff': False, 'velocity': 1, 't': 6.1},
    {'note': 'A4', 'onoff': True, 'velocity': 1, 't': 6.1},
    {'note': 'A4', 'onoff': False, 'velocity': 1, 't': 7.1},
    {'note': 'B4', 'onoff': True, 'velocity': 1, 't': 7.1},
    {'note': 'B4', 'onoff': False, 'velocity': 1, 't': 8.1},
]

canon3 = [
    {'note': 'G5', 'onoff': True, 'velocity': 1, 't': 0.1},
    {'note': 'G5', 'onoff': False, 'velocity': 1, 't': 1.1},
    {'note': 'D5', 'onoff': True, 'velocity': 1, 't': 1.1},
    {'note': 'D5', 'onoff': False, 'velocity': 1, 't': 2.1},
    {'note': 'E5', 'onoff': True, 'velocity': 1, 't': 2.1},
    {'note': 'E5', 'onoff': False, 'velocity': 1, 't': 3.1},
    {'note': 'B4', 'onoff': True, 'velocity': 1, 't': 3.1},
    {'note': 'B4', 'onoff': False, 'velocity': 1, 't': 4.1},
    {'note': 'C5', 'onoff': True, 'velocity': 1, 't': 4.1},
    {'note': 'C5', 'onoff': False, 'velocity': 1, 't': 5.1},
    {'note': 'G4', 'onoff': True, 'velocity': 1, 't': 5.1},
    {'note': 'G4', 'onoff': False, 'velocity': 1, 't': 6.1},
    {'note': 'C5', 'onoff': True, 'velocity': 1, 't': 6.1},
    {'note': 'C5', 'onoff': False, 'velocity': 1, 't': 7.1},
    {'note': 'D5', 'onoff': True, 'velocity': 1, 't': 7.1},
    {'note': 'D5', 'onoff': False, 'velocity': 1, 't': 8.1},
]

canon0 = [
    {'note': 'E6', 'onoff': True, 'velocity': 1, 't': 0.1},
    {'note': 'E6', 'onoff': False, 'velocity': 1, 't': 1.1},
    {'note': 'D6', 'onoff': True, 'velocity': 1, 't': 1.1},
    {'note': 'D6', 'onoff': False, 'velocity': 1, 't': 2.1},
    {'note': 'C6', 'onoff': True, 'velocity': 1, 't': 2.1},
    {'note': 'C6', 'onoff': False, 'velocity': 1, 't': 3.1},
    {'note': 'B5', 'onoff': True, 'velocity': 1, 't': 3.1},
    {'note': 'B5', 'onoff': False, 'velocity': 1, 't': 4.1},
    {'note': 'A5', 'onoff': True, 'velocity': 1, 't': 4.1},
    {'note': 'A5', 'onoff': False, 'velocity': 1, 't': 5.1},
    {'note': 'G5', 'onoff': True, 'velocity': 1, 't': 5.1},
    {'note': 'G5', 'onoff': False, 'velocity': 1, 't': 6.1},
    {'note': 'A5', 'onoff': True, 'velocity': 1, 't': 6.1},
    {'note': 'A5', 'onoff': False, 'velocity': 1, 't': 7.1},
    {'note': 'B5', 'onoff': True, 'velocity': 1, 't': 7.1},
    {'note': 'B5', 'onoff': False, 'velocity': 1, 't': 8.1},
]


def multiply(op1, op2):
    assert isinstance(op1, Operator)
    if isinstance(op2, numbers.Number):
        op2 = ConstOperator(op2, op1.sr, op1.buffer_size)
    return ReduceOperator(
        input_ops=[(op1, 0), (op2, 0)], operation=ReduceOperator.ReduceOperations.MUL)


def const(val):
    return ConstOperator(constant=val, sr=sr, buffer_size=buffer_size)


def add(op1, *args):
    assert isinstance(op1, Operator)
    others = []
    for arg in args:
        if isinstance(arg, numbers.Number):
            arg = ConstOperator(arg, op1.sr, op1.buffer_size)
        others.append((arg, 0))
    return ReduceOperator(
        input_ops=[(op1, 0), *others], operation=ReduceOperator.ReduceOperations.SUM)


midi0 = MIDIInput(note_seq=canon0, gui=gui, sr=sr, buffer_size=buffer_size, bpm=45, volume=0.37)
midi1 = MIDIInput(note_seq=canon1, sr=sr, buffer_size=buffer_size, bpm=45, volume=0.2)
midi2 = MIDIInput(note_seq=canon2, sr=sr, buffer_size=buffer_size, bpm=45, volume=0.1)
midi3 = MIDIInput(note_seq=canon3, sr=sr, buffer_size=buffer_size, bpm=45, volume=0.1)
midi_bass = MIDIInput(note_seq=canon_bass, sr=sr, buffer_size=buffer_size, bpm=45, volume=0.1)

scope100 = Oscilloscope(gui=gui, y_range=(0, 1000), input_ops=[(midi3, 0)], name='MIDI Freq')
scope101 = Oscilloscope(gui=gui, y_range=range_1, input_ops=[(midi3, 1)], name='MIDI Amp')

one = const(1)
zero = const(0)

amp_lfo = Oscillator(
    input_ops=[
        (const(3), 0),
        (const(0.25), 0),
        (zero, 0)],
    osc_type='sine',
    name='Sine LFO')
sine_lfo_scope = Oscilloscope(input_ops=[(amp_lfo, 0)], y_range=range_1, gui=gui, name='LFO')

freq_lfo = Oscillator(
    input_ops=[
        (const(2), 0),
        (const(0.2), 0),
        (zero, 0)],
    osc_type='square',
    name='Sine LFO 2')

osc0 = Oscillator(input_ops=[(add(midi0, freq_lfo), 0), (midi0, 1), (zero, 0)],
                  osc_type='square',
                  name='Square0')
osc0_scope = Oscilloscope(input_ops=[(osc0, 0)], y_range=range_1, gui=gui, name='Osc1 Out')

osc1 = Oscillator(input_ops=[(midi1, 0), (midi1, 1), (zero, 0)], osc_type='saw', name='Saw1')
osc2 = Oscillator(input_ops=[(midi2, 0), (midi2, 1), (zero, 0)], osc_type='saw', name='Saw2')
osc3 = Oscillator(input_ops=[(midi3, 0), (midi3, 1), (zero, 0)], osc_type='saw', name='Saw3')
osc_bass = Oscillator(input_ops=[(midi_bass, 0), (midi_bass, 1), (zero, 0)], osc_type='sine', name='Sine Bass')

osc = add(osc_bass, osc1, osc2, osc3, osc0)

# la la la sound >_<!!!
fm = add(osc, amp_lfo)

scope_before = Oscilloscope(input_ops=[(fm, 0)], y_range=range_1, gui=gui, name='Before-filter Oscilloscope')
filtered = FIRFilter(input_ops=[(fm, 0)],
                     bands=[(2000, 1), (2001, 8000, 0.25), (8001, 20000, 0.1)],
                     window_func=np.hamming,
                     filter_size=buffer_size,
                     gui=gui,
                     name='FIRFilter')
scope_after = Oscilloscope(input_ops=[(filtered, 0)], y_range=range_1, gui=gui, name='After-filter Oscilloscope')

limiter = Limiter(input_ops=[(filtered, 0)])
dft = DFT(input_ops=[(limiter, 0)])
scope_freq_after = Oscilloscope(input_ops=[(dft, 0)],
                                x_range=(30, 15000),
                                x_max=dft.get_cut_frequency(),
                                x_log=True,
                                y_db=True,
                                y_range=(-50, 0), gui=gui,
                                name='After-filter Freq')
out = DeviceOutput(input_ops=[(filtered, 0)], volume=1)

gui.post_init(out)

player = play.Player(sr, buffer_size, (out, 0), [out, scope100, scope101, scope_before, scope_after,
                                                 osc0_scope, scope_freq_after, sine_lfo_scope])
# player.save('a.wav', 5)
player.play_non_blocking()


gui.start()

