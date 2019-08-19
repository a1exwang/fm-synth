import numpy as np
import os
import numbers

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


one = const(1)
zero = const(0)

left = Oscillator(
    input_ops=[
        (ConstOperator(constant=440, sr=sr, buffer_size=buffer_size, name='f-left', range=(0, 500), step=0.1), 0),
        (const(0.25), 0),
        (zero, 0)],
    osc_type='sine',
    name='Left')
scope_left = Oscilloscope(input_ops=[(left, 0)], y_range=range_1, gui=gui, name='Left scope')
right = Oscillator(
    input_ops=[
        (ConstOperator(constant=444, sr=sr, buffer_size=buffer_size, name='f-right', range=(0, 500), step=0.1), 0),
        (const(0.25), 0),
        (zero, 0)],
    osc_type='sine',
    name='Right')
scope_right = Oscilloscope(input_ops=[(right, 0)], y_range=range_1, gui=gui, name='Right scope')
out = DeviceOutput(input_ops=[(left, 0), (right, 0)], volume=1)

gui.post_init(out)

player = play.Player(sr, buffer_size, (out, 0), [out, scope_left, scope_right])
player.play_non_blocking()
gui.start()

