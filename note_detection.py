import numbers
import numpy as np
import os

from gui.monitors import FMSynthGUI
from operators.const import ConstOperator
from operators.base import Operator
from operators.device_output import DeviceOutput
from operators.reduce import ReduceOperator
from operators.oscillator import Oscillator
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


def make_wavelet(a, phi, t):
    return lambda f: a * np.sin(2 * np.pi * f * t + phi)


def func(f, a, phi, t):
    fn = make_wavelet(a, phi, t)
    formants = (2, 3, 4, 5)
    s = np.zeros(np.shape(t))
    for formant in formants:
        s += fn(formant * f)
    return s / len(formants)


op = Oscillator(
    input_ops=[
        (ConstOperator(constant=440, sr=sr, buffer_size=buffer_size, name='f-op', range=(0, 500), step=0.1), 0),
        (const(0.25), 0),
        (zero, 0)],
    osc_type=func,
    name='Op1')
ref = Oscillator(
    input_ops=[
        (ConstOperator(constant=880, sr=sr, buffer_size=buffer_size, name='f-ref', range=(0, 1000), step=0.1), 0),
        (const(0.25), 0),
        (zero, 0)],
    osc_type='sine',
    name='Reference')
scope_1 = Oscilloscope(input_ops=[(op, 0)], y_range=range_1, gui=gui, name='Scope1')
out = DeviceOutput(input_ops=[(op, 0), (ref, 0)], volume=1)

gui.post_init(out)

player = play.Player(sr, buffer_size, (out, 0), [out, scope_1])
player.play_non_blocking()
gui.start()

