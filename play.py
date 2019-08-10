import pyaudio


class Player:
    def __init__(self, sr, buffer_size, input_op, all_output_operators):
        self.input_op = input_op
        self.all_output_operators = all_output_operators
        self.current_offset = 0
        self.stream = None
        self.buffer_size = buffer_size
        self.sr = sr

    def callback(self, in_data, frame_count, time_info, flag):
        if flag:
            print("Playback Error: %i" % flag)
        assert(frame_count == self.buffer_size)
        self.current_offset += 1
        for op in self.all_output_operators:
            op.step(self.current_offset + 1)

        result = self.input_op[0].output_buffers[self.input_op[1]]
        return result.tobytes(), pyaudio.paContinue

    def play_non_blocking(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(format=pyaudio.paInt16,
                              channels=2,
                              rate=self.sr,
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
                         rate=self.sr,
                         output=True)

        data, state = self.callback(None, self.buffer_size, 0, None)
        while state == pyaudio.paContinue:
            stream.write(data)
            data, state = self.callback(None, self.buffer_size, 0, None)

        stream.close()
        pa.terminate()

