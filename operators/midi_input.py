import numpy as np
from operators.base import InputOperator
import functools
from channels.channel import Channel


class MIDIInput(InputOperator):
    DEFAULT_NOTES = [
        {'note': 'C5', 'onoff': True,  'velocity': 1, 't': 0.1},
        {'note': 'C5', 'onoff': False, 'velocity': 1, 't': 1.1},
        {'note': 'G4', 'onoff': True,  'velocity': 1, 't': 1.1},
        {'note': 'G4', 'onoff': False, 'velocity': 1, 't': 2.1},
        {'note': 'A4', 'onoff': True,  'velocity': 1, 't': 2.1},
        {'note': 'A4', 'onoff': False, 'velocity': 1, 't': 3.1},
        {'note': 'E4', 'onoff': True,  'velocity': 1, 't': 3.1},
        {'note': 'E4', 'onoff': False, 'velocity': 1, 't': 4.1},
        {'note': 'F4', 'onoff': True,  'velocity': 1, 't': 4.1},
        {'note': 'F4', 'onoff': False, 'velocity': 1, 't': 5.1},
        {'note': 'C4', 'onoff': True,  'velocity': 1, 't': 5.1},
        {'note': 'C4', 'onoff': False, 'velocity': 1, 't': 6.1},
        {'note': 'F4', 'onoff': True,  'velocity': 1, 't': 6.1},
        {'note': 'F4', 'onoff': False, 'velocity': 1, 't': 7.1},
        {'note': 'G4', 'onoff': True,  'velocity': 1, 't': 7.1},
        {'note': 'G4', 'onoff': False, 'velocity': 1, 't': 8.1},
    ]

    input_count = 0
    output_count = 2

    def __init__(self, gui, sr=44100, buffer_size=2048, bpm=120,
                 note_seq=DEFAULT_NOTES, loop=True,
                 adsr=(1, 1, 1, 1),
                 volume=1.0,
                 name='MIDIInput'):
        super().__init__(sr, buffer_size, volume, name)
        self.gui = gui
        self.bpm = bpm
        self.bps = bpm / 60.0
        self.adsr = np.array(adsr)
        self.note_seq = note_seq
        self.loop = loop

        self.sustain_level = 0.5
        self.peak_level = 0.9
        self.sustain_rate = 0
        self.attack_base_duration = 0.05
        self.decay_base_duration = 0.05
        self.sustain_base_duration = 2
        self.release_base_duration = 0.3

        self.ads_env = self.ads_envelope()
        self.release_env = self.release_envelope()

        self.first_note_index = 0

        if self.gui is not None:
            self.pl = self.gui.add_plot(self.name + "ASDR envelope")
            self.curve = self.pl.plot(pen='y')
            x = np.arange(len(self.ads_env)) / self.sr
            y = self.ads_env

            self.curve.setData(x, y)
            self.pl.setLabel('left', "Volume", units='dB')
            self.pl.setLabel('bottom', "t", units='s')
            self.pl.enableAutoRange('xy', False)

            self.channel = Channel.get_instance()
            self.channel.add_channel(name='InputVol', slot=self.volume_changed, get_val=lambda: self.volume)

    @staticmethod
    def note_name_to_midi_value(name):
        notes = [["C"], ["C#", "Db"], ["D"], ["D#", "Eb"], ["E"],
                 ["F"], ["F#", "Gb"], ["G"], ["G#", "Ab"], ["A"],
                 ["A#", "Bb"], ["B"]]
        letter = name[0].upper()
        i = 0
        answer = 0
        for note in notes:
            for form in note:
                if letter == form:
                    answer = i
                    break
            i += 1
        # Octave
        answer += (int(name[-1])) * 12
        return answer

    @staticmethod
    def midi_value_to_freq(midi_val):
        return 440 * 2.0**((midi_val - 69) / 12.0)

    def next_buffer(self, caller, current_count):
        arr_freq = np.zeros([self.buffer_size])
        arr_amp = np.zeros([self.buffer_size])

        begin, end = None, None
        for i, note in enumerate(self.note_seq):
            if current_count > self.beats_to_index(note['t']):
                begin = i
            elif current_count <= self.beats_to_index(note['t']) < current_count + self.buffer_size:
                end = i
            else:
                break
        if end is None and begin is not None:
            end = begin
        if begin is None and end is not None:
            begin = end

        if begin is None and end is None:
            return [arr_freq, arr_amp]

        for i in range(begin, end):
            note = self.note_seq[i+1]
            last = self.note_seq[i]
            i1, i2 = self.beats_to_index(last['t']) - current_count, self.beats_to_index(note['t']) - current_count
            i1 = max(i1, 0)
            if last['onoff'] is True:
                # last ~ note 之间是 Sustain 过程
                arr_freq[i1:i2] = self.note_name_to_freq(last['note'])
                arr_amp[i1:i2] = self.ads_env[:(i2-i1)] * last['velocity']
            else:
                # last ~ note 之间是 Release 过程
                arr_freq[i1:i2] = self.note_name_to_freq(last['note'])
                arr_amp[i1:i2] = self.release_env[:(i2-i1)] * last['velocity']

        # 上面的循环过后，还剩下一段未处理
        note = self.note_seq[end]
        i1 = self.beats_to_index(note['t']) - current_count
        if i1 < 0:
            arr_freq[:] = self.note_name_to_freq(note['note'])
            env_start = -i1
            if self.note_seq[end]['onoff'] is True:
                if self.buffer_size + env_start > len(self.ads_env):
                    valid = self.buffer_size + env_start - len(self.ads_env)
                    if valid > len(arr_amp):
                        arr_amp[:] = 0
                    else:
                        arr_amp[:valid] = self.ads_env[env_start:env_start+valid]
                        arr_amp[valid:] = 0
                else:
                    arr_amp[:] = self.ads_env[env_start:env_start+self.buffer_size] * note['velocity']
            else:
                if self.buffer_size + env_start > len(self.release_env):
                    valid = self.buffer_size + env_start - len(self.release_env)
                    if valid > len(arr_amp):
                        arr_amp[:] = 0
                    else:
                        arr_amp[:valid] = self.release_env[env_start:env_start+valid]
                        arr_amp[valid:] = 0
                else:
                    arr_amp[:] = self.release_env[env_start:env_start+self.buffer_size] * note['velocity']

        else:
            arr_freq[i1:] = self.note_name_to_freq(note['note'])
            if self.note_seq[end]['onoff'] is True:
                arr_amp[i1:] = self.ads_env[:self.buffer_size-i1] * note['velocity']
            else:
                arr_amp[i1:] = self.release_env[:self.buffer_size-i1] * note['velocity']
        return [arr_freq, arr_amp * self.volume]

    def ads_envelope(self):
        n = int(self.sr * 2)
        envelope = np.zeros([n], dtype='float32')
        for t in range(n):
            attack_l, decay_l, sustain_l, release_l = \
                np.array(self.adsr * self.sr * [self.attack_base_duration,
                                                self.decay_base_duration,
                                                self.sustain_base_duration,
                                                self.release_base_duration], dtype='int32')
            if t < attack_l:
                envelope[t] = t / attack_l * self.peak_level
            elif t < attack_l + decay_l:
                envelope[t] = self.peak_level - (t - attack_l) / decay_l * (self.peak_level - self.sustain_level)
            else:
                envelope[t] = max(self.sustain_level - ((t - attack_l - decay_l) / sustain_l) * self.sustain_rate, 0)

        return envelope

    def release_envelope(self):
        attack_l, decay_l, sustain_l, release_l = \
            np.array(self.adsr * self.sr * [0.1, 0.1, 3, 0.1], dtype='int32')
        envelope = np.zeros([release_l], dtype='float32')
        # release
        for t in range(release_l):
            envelope[t] = self.sustain_level * (1 - t / release_l)
        return envelope

    def beats_to_index(self, beat):
        return int(beat / self.bps * self.sr)

    def note_name_to_freq(self, name):
        return self.midi_value_to_freq(self.note_name_to_midi_value(name))
