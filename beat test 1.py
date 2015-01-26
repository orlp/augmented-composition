import midiwriter

import random
import math

PATTERNS = [[0.5, 0.5], [0.25, 0.25, 0.5], [0.5, 0.25, 0.25]]
SUBDIVISION_STEPS = 1
UNIFORMITY = 100
NUM_MEASURES = 40
NUM_MUTATIONS = 3
INSTRUMENT = 45

class Note(object):
    def __init__(self, duration):
        self.duration = duration

def weighed_choice(notes):
    l = []
    for note in notes:
        if note.duration >= 120:
            for i in range(int(math.log(note.duration, 2)*UNIFORMITY)):
                l.append(note)
    return random.choice(l)

beat = []
for i in range(4):
    beat.append(Note(480))

for i in range(SUBDIVISION_STEPS):
    note = weighed_choice(beat)
    pattern = random.choice(PATTERNS)
    for fraction in pattern:
        beat.insert(beat.index(note), Note(note.duration*fraction))
    beat.remove(note)

first_measure = beat[:]
song = first_measure[:]

for i in range(NUM_MEASURES):
    print([note.duration for note in beat])
    for j in range(NUM_MUTATIONS):
        note = weighed_choice(beat)
        pattern = random.choice(PATTERNS)
        for fraction in pattern:
            beat.insert(beat.index(note), Note(note.duration*fraction))
        print(pattern, note.duration)
        beat.remove(note)

    song.extend(beat)
    beat = first_measure[:]

    print("\n\n\n")
writer = midiwriter.MIDIWriter()
for note in song:
    writer.note_on(0, 9, INSTRUMENT)
    writer.note_off(int(note.duration), 9, INSTRUMENT)

writer.write_to_file(open("test.mid", "wb"))

for note in song:
    print(note.duration)
