from PyQt5.QtCore import pyqtSlot
from channels.channel import Channel
from operators.base import OutputOperator
import numpy as np
import pyaudio


class DeviceOutput(OutputOperator):
    input_count = 1

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

    @staticmethod
    def build(ops, m):
        assert m['type'] == 'DeviceOutput'

    def next_buffer(self, input_buffers, n):
        mixed = input_buffers[0]
        arr = np.array(mixed, dtype='float32') * 2**16
        arr = np.transpose(np.array([arr, arr]))
        result = np.array(arr, dtype='int16')
        return [result * self.volume]

    def callback(self, in_data, frame_count, time_info, flag):
        if flag:
            print("Playback Error: %i" % flag)
        assert(frame_count == self.buffer_size)
        self.step(self.current_offset + 1)
        result = self.output_buffers[0]
        return result.tobytes(), pyaudio.paContinue

    def play_non_blocking(self):
        pa = pyaudio.PyAudio()

        self.stream = pa.open(format=pyaudio.paInt16,
                              channels=2,
                              rate=44100,
                              output=True,
                              frames_per_buffer=self.buffer_size,
                              stream_callback=self.callback)

        # while stream.is_active():
        #     time.sleep(0.1)
        #
        # stream.close()
        # pa.terminate()

    def play(self):
        pa = pyaudio.PyAudio()

        stream = pa.open(format=pyaudio.paInt16,
                         channels=2,
                         rate=44100,
                         output=True)

        data, state = self.callback(None, self.buffer_size, 0, None)
        while state == pyaudio.paContinue:
            stream.write(data)
            data, state = self.callback(None, self.buffer_size, 0, None)

        stream.close()
        pa.terminate()

