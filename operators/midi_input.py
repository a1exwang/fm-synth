import numpy as np
from operators.base import InputOperator
import functools


class MIDIInput(InputOperator):
    PACHELBEL_CANON_CHORDS = [
        ['C5', 'E5', 'G5'],
        ['G4', 'B4', 'D5'],
        ['A4', 'C5', 'E5'],
        ['E4', 'G4', 'B4'],
        ['F4', 'A4', 'C5'],
        ['C4', 'E4', 'G4'],
        ['F4', 'A4', 'C5'],
        ['G4', 'B4', 'D5'],
    ]
    input_count = 0
    output_count = 2

    def __init__(self, sr=44100, buffer_size=2048, bpm=120,
                 notes=PACHELBEL_CANON_CHORDS, loop=True, volume=1.0,
                 name='MIDIInput'):
        super().__init__(sr, buffer_size, volume, name)
        self.bpm = bpm
        self.bps = bpm / 60.0
        self.note_names = notes
        self.notes = np.zeros(np.shape(notes))
        for i, notes_at_t in enumerate(notes):
            for j, note in enumerate(notes_at_t):
                self.notes[i, j] = self.midi_value_to_freq(self.note_name_to_midi_value(note))

        self.loop = loop

    @staticmethod
    def note_name_to_midi_value(name):
        notes = [["C"],["C#","Db"],["D"],["D#","Eb"],["E"],["F"],["F#","Gb"],["G"],["G#","Ab"],["A"],["A#","Bb"],["B"]]
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
        arr_amp = 0.5 * np.ones([self.buffer_size])
        for i in range(self.buffer_size):
            n_beat = int(((i+current_count)/self.sr) * self.bps)
            if self.loop:
                n_beat %= len(self.note_names)
            if n_beat > len(self.note_names):
                raise StopIteration
            arr_freq[i] = self.notes[n_beat][0]

        return [arr_freq, arr_amp]
