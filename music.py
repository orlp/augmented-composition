import midi

class Song(object):
    def __init__(self):
        self.instruments = []

    def add_instrument(self, instrument):
        self.instruments.append(instrument)

    def write_to_file(self, stream):
        writer = midi.MIDIWriter()
        events = []
        programs = {}
        free_channel = 0

        for instrument in self.instruments:
            if instrument.is_drum: channel = 9
            else:
                channel = free_channel
                free_channel += 1
                if free_channel == 9: free_channel = 10

            programs[channel] = instrument.program

            for time_offset, pitch, duration, velocity, in instrument.notes:
                events.append((int(time_offset * 480), "on", channel, pitch, velocity))
                events.append((int((time_offset + duration) * 480), "off", channel, pitch, velocity))

        for channel, program in programs.items():
            writer.program_change(0, channel, program)


        events.sort()
        last_time_offset = 0
        for time_offset, onoff, channel, pitch, velocity in events:
            delta_time = time_offset - last_time_offset

            if onoff == "on": writer.note_on(delta_time, channel, pitch, velocity)
            else:             writer.note_off(delta_time, channel, pitch, velocity)

            last_time_offset = time_offset

        writer.write_to_file(stream)


class Instrument(object):
    def __init__(self, program, is_drum=False):
        self.program = program
        self.notes = []
        self.is_drum = is_drum

    def play_note(self, time_offset, pitch, duration=1, velocity=64):
        self.notes.append((time_offset, pitch, duration, velocity))
        

piano = Instrument(0)
for i in range(4):
    piano.play_note(4*i+0, 64, 1)
    piano.play_note(4*i+1, 66, 1)
    piano.play_note(4*i+2, 68, 1)
    piano.play_note(4*i+3, 69, 1)

drums = Instrument(0, True)
for i in range(16):
    drums.play_note(i, 35)
    drums.play_note(i, 42)
    drums.play_note(i + 0.5, 42)

song = Song()
song.add_instrument(piano)
song.add_instrument(drums)
song.write_to_file(open("test.mid", "wb"))
