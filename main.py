from scamp import *
from mido import MidiFile, tick2second, MidiTrack, bpm2tempo, tempo2bpm
from structure_parser import *
import sys


s = Session()
# piano = s.new_part('church organ')  # pt little fugue
piano = s.new_part('piano')
# piano = s.new_part('clarinet')
# piano = s.new_part('guitar')

# fugue = MidiFile('outputs/result1.midi')
# tempo = 0
# fugue.ticks_per_beat = 240
# fugue.save("outputs/result1.midi")


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


tempo = 600000

# for track in midi_tracks:
#     s.fork(play_track, args=([track]))
#
# s.wait_for_children_to_finish()
# print(midi_tracks)

"""                                            IMPORTANT 


"""


def generate_fugue(subject_path, structure_path, output_path, output_name, index=-1):
    all_tracks = build_fugue(subject_path, structure_path)
    print("fugue built")
    midi_tracks = get_midi_tracks(all_tracks)
    print("midi tracks prepared")
    output = output_path + '\\' + output_name
    if index != -1:
        output += str(index)
    output += ".midi"
    export_fugue(midi_tracks, output)
    print(output, "done!")


# generate_fugue("test_subjects/fairouz.txt", "structures/3-part.txt", "prezentare", "fairouz2")

print(sys.argv)
print(sys.prefix != sys.base_prefix)
print("merge")

if len(sys.argv) == 6:
    subjectPath = sys.argv[1]
    structurePath = sys.argv[2]
    numberOfFiles = sys.argv[3]
    outputPath = sys.argv[4]
    outputName = sys.argv[5]

    if int(numberOfFiles) == 1:
        generate_fugue(subjectPath, structurePath, outputPath, outputName)
    else:
        for i in range(int(numberOfFiles)):
            generate_fugue(subjectPath, structurePath, outputPath, outputName, i+1)


# file_names = [
#     "kingdom_of_cold_flesh.txt",
#     "nothing_else_matters.txt",
#     "seven_nation.txt",
#     "smoke_on the_water.txt",
#     "soul_kitchen.txt",
#     "subject.txt",
#     "subject_bwv_846.txt",
#     "subject_bwv_848.txt",
#     "subject_bwv_853.txt",
#     "subject_bwv_861.txt",
#     "subject_little_fugue.txt",
#     "sweet_child_o_mine.txt",
# ]
#
# for name in file_names:
#     s_file = open("test_subjects/" + name)
#     subject = Subject(s_file)
#     key, is_major = get_key_formatted_from_notes(subject.notes)
#     print(name, key, "major" if is_major else "minor")
