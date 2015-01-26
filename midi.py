import struct
import collections


class MIDIWriter(object):
    MIDIEvent = collections.namedtuple("MIDIEvent",
                                       ("delta_time", "type", "channel", "data"))

    def __init__(self):
        self.events = []

    def note_off(self, ticks, channel, note, velocity=64):
        self.events.append(self.MIDIEvent(ticks, 0x8, channel, struct.pack(">BB", note, velocity)))

    def note_on(self, ticks, channel, note, velocity=64):
        self.events.append(self.MIDIEvent(ticks, 0x9, channel, struct.pack(">BB", note, velocity)))

    def program_change(self, ticks, channel, program):
        self.events.append(self.MIDIEvent(ticks, 0xC, channel, struct.pack(">B", program)))

    def write_to_file(self, stream):
        header_length = 6
        fmt = 1
        tracks = 1
        division = 480 
        stream.write(b"MThd")
        stream.write(struct.pack(">IHHH", header_length, fmt, tracks, division))

        encoded_events = []
        for event in self.events:
            encoded_event = self.encode_varlen(event.delta_time)
            encoded_event += bytes([(event.type << 4) | event.channel])
            encoded_event += event.data
            encoded_events.append(encoded_event)

        buf = b"".join(encoded_events)
        buf += bytes([2, 0xff, 0x2f, 0]) # end of track, 2 ticks space
        stream.write(b"MTrk")
        stream.write(struct.pack(">I", len(buf)))
        stream.write(buf)
    
    def encode_varlen(self, value):
        res = [value & 0x7F]
        value >>= 7

        while value:
            res.insert(0, (value & 0x7F) | 0x80)
            value >>= 7

        return bytes(res)


# 480 ticks per quarter note
# 500000 microseconds (0.5s) per quarter note

writer = MIDIWriter()
for i in range(30, 90):
    writer.note_on(0, 9, i)
    writer.note_off(480//4, 9, i)
writer.program_change(0, 9, 48)
for i in range(30, 90):
    writer.note_on(0, 9, i)
    writer.note_off(480//4, 9, i)
writer.write_to_file(open("test.mid", "wb"))
