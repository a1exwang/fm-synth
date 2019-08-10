from PyQt5.QtCore import pyqtSlot
from channels.channel import Channel
from operators.base import OutputOperator
import numpy as np


class DeviceOutput(OutputOperator):
    def __init__(self, input_op, volume=1.0, name='DeviceOutput'):
        super().__init__((input_op,), name)
        self.total_count = 0
        self.stream = None
        self.volume = volume

        self.channel = Channel.get_instance()
        self.channel.add_channel(name='MasterVol', slot=self.volume_changed, get_val=lambda: self.volume)

    @pyqtSlot(float, name='volume_changed')
    def volume_changed(self, vol):
        if vol <= 0:
            vol = 0
        if vol >= 1:
            vol = 1
        self.volume = vol

    def next_buffer(self, input_buffers, n):
        mixed = input_buffers[0]
        arr = np.array(mixed, dtype='float32') * 2**16
        arr = np.transpose(np.array([arr, arr]))
        result = np.array(arr, dtype='int16')
        return [result * self.volume]
