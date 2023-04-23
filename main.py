from scamp import *
from mido import MidiFile, tick2second, MidiTrack

s = Session()
piano = s.new_part('piano')
# piano.play_note(60, 0.8, 1) # C4
# piano.play_note(72, 0.8, 1)
# piano.play_note(84, 0.8, 1)

modes = {
    'major': [0, 2, 4, 5, 7, 9, 11],
    'minor': [0, 2, 3, 5, 7, 8, 10],
}

note_value = {
    'C': 60,
    'C#': 61,
    'D': 62,
    'D#': 63,
    'E': 64,
    'F': 65,
    'F#': 66,
    'G': 67,
    'G#': 68,
    'A': 69,
    'A#': 70,
    'B': 71,
}


def play_scale(note, mode):
    for interval in modes[mode]:
        piano.play_note(note_value[note] + interval, 0.8, 0.5)
    piano.play_note(note_value[note] + 12, 0.8, 0.5)


# play_scale('E', 'minor')

fugue = MidiFile('Fugue1.mid')
# print(fugue)
tempo = 0


def process_track(track: MidiTrack):
    global tempo
    notes_playing = {}
    for msg in track:
        wait(tick2second(msg.time, fugue.ticks_per_beat, tempo), "time")
        if msg.is_meta:
            if msg.type == 'set_tempo':
                tempo = msg.tempo
        else:
            if msg.type == 'note_on':
                notes_playing[msg.note] = piano.start_note(msg.note, msg.velocity / 127)
            elif msg.type == 'note_off':
                if msg.note in notes_playing:
                    piano.end_note(notes_playing[msg.note])
                    notes_playing.pop(msg.note)


for track in fugue.tracks:
    s.fork(process_track, args=([track]))

s.wait_for_children_to_finish()
print(tempo)

