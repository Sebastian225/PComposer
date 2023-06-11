from scamp import *
from mido import MidiFile, tick2second, MidiTrack, bpm2tempo, tempo2bpm
from fugue import *
from key_finder import *
from counterpoint import *
from structure_parser import *

s = Session()
# piano = s.new_part('church organ')  # pt little fugue
piano = s.new_part('piano')
# piano = s.new_part('clarinet')
# piano = s.new_part('guitar')
# piano.play_note(60, 0.8, 1) # C4
# piano.play_note(72, 0.8, 1)
# piano.play_note(84, 0.8, 1)

# modes = {
#     'major': [0, 2, 4, 5, 7, 9, 11],
#     'minor': [0, 2, 3, 5, 7, 8, 10],
# }


# def play_scale(note, mode):
#     for interval in modes[mode]:
#         piano.play_note(note_value[note] + interval, 0.8, 0.5)
#     piano.play_note(note_value[note] + 12, 0.8, 0.5)


# play_scale('E', 'minor')

fugue = MidiFile('outputs/result1.midi')
tempo = 0
fugue.ticks_per_beat = 240
fugue.save("outputs/result1.midi")


def play_track(track: MidiTrack):
    global tempo
    notes_playing = {}
    for msg in track:
        wait(tick2second(msg.time, 240, tempo), "time")
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


# for track in fugue.tracks:
#     s.fork(play_track, args=([track]))
#
# s.wait_for_children_to_finish()

input_file = open("test_subjects/subject.txt")  # C minor
# input_file = open("test_subjects/test.txt")  # G major
# input_file = open("test_subjects/subject_bwv_846.txt")  # C major
# input_file = open("test_subjects/subject_bwv_848.txt")  # C# major
# input_file = open("test_subjects/subject_bwv_853.txt")  # D# minor (Eb minor)
# input_file = open("test_subjects/subject_little_fugue.txt")  # G minor
# input_file = open("test_subjects/subject_bwv_861.txt")  # G minor, alg crede ca e A# major adica relativa
# input_file = open("test_subjects/kingdom_of_cold_flesh.txt")  # A# minor
# input_file = open("test_subjects/nothing_else_matters.txt")  # E minor

# subject = Subject(input_file)
# answer = Answer(subject, True)
# bass_subject = modulate(subject.notes, "C", "C", "down")
# messages_list = []
# for note in subject.notes:
#     messages_list.extend(note.get_midi_messages())

# for note in answer.notes:
#     messages_list.extend(note.get_midi_messages())
#
# for note in bass_subject:
#     messages_list.extend(note.get_midi_messages())
# relative_notes = modulate(modulate_to_relative(subject.notes, "E", False), "G", "E", "up")
# relative_notes = modulate(relative_notes, "E", "E", "up")
# for note in relative_notes:
#     messages_list.extend(note.get_midi_messages())

# every track must have this, will make a function later
# messages_list[0].time += 120

tempo = 600000

# print(get_key(get_score(get_input_vector(subject.notes))))

# cs = generate_counterpoint(subject.notes, key, is_major)
# cs = generate_random_genome_from_notes(subject.notes)
# get_pitches_list(cs, subject.notes)
# cs = generate_counterpoint(subject.notes)


# write_notes(cs)

# cs_messages = []
# for note in cs:
#     cs_messages.extend(note.get_midi_messages())
#
# cs_messages[0].time += 120

# cs2 = generate_counterpoint(cs)
# cs2_messages = []
# for note in cs2:
#     cs2_messages.extend(note.get_midi_messages())
#
# cs2_messages[0].time += 120

# print(get_pitches_list(cs, subject.notes))

# parse_structure("structures/3-part.txt")
# key, is_major = get_key_formatted_from_notes(subject.notes)
# relative_subject = modulate_to_relative(subject.notes, key, is_major)
# rs_msg = []
# for note in relative_subject:
#     # print(note.pitch)
#     rs_msg.extend(note.get_midi_messages())

# play_track(MidiTrack(messages_list))
# play_track(MidiTrack(rs_msg))

# play_track(MidiTrack(messages_list))
# s.fork(play_track, args=([MidiTrack(messages_list)]))
# s.fork(play_track, args=([MidiTrack(cs_messages)]))
# s.wait_for_children_to_finish()
# play_track(MidiTrack(cs_messages))
#
# s.fork(play_track, args=([MidiTrack(messages_list)]))
# s.fork(play_track, args=([MidiTrack(cs_messages)]))
# s.fork(play_track, args=([MidiTrack(cs2_messages)]))
# s.wait_for_children_to_finish()

all_tracks = build_fugue("test_subjects/subject.txt", "structures/3-part.txt")
midi_tracks = get_midi_tracks(all_tracks)
for track in midi_tracks:
    s.fork(play_track, args=([track]))

s.wait_for_children_to_finish()
print(midi_tracks)
export_fugue(midi_tracks)
