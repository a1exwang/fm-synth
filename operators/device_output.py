import time
import numpy as np
import pyaudio
from operators.base import OutputOperator


class DeviceOutput(OutputOperator):
    input_count = 1

    def __init__(self, input_op, volume=1.0, name='DeviceOutput'):
        super().__init__((input_op,), volume, name)
        self.total_count = 0
        self.stream = None

    def next_buffer(self, caller, n):
        outs = super().next_buffer(self, n)
        mixed = outs[0]
        arr = np.array(mixed, dtype='float32') * 2**16
        arr = np.transpose(np.array([arr, arr]))
        result = np.array(arr, dtype='int16')
        self.total_count += self.buffer_size
        return result

    def callback(self, in_data, frame_count, time_info, flag):
        if flag:
            print("Playback Error: %i" % flag)
        assert(frame_count == self.buffer_size)
        result = self.next_buffer(self, self.total_count)
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
