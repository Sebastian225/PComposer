import random

from mido import MidiTrack, MidiFile, MetaMessage

from constants import *
from counterpoint import get_total_duration, generate_counterpoint
from fugue import *
from key_finder import get_key_formatted_from_notes


def get_melody_ranges(nr_of_parts: int):
    if nr_of_parts == 3:
        return [('B3', 'C6'), ('G3', 'E5'), ('D2', 'E4')]
    return [('B3', 'C6'), ('G3', 'E5'), ('C3', 'B4'), ('D2', 'E4')]


def write_notes(notes):
    f = open("outputs/countersubjects.txt", "a")
    f.write("COUNTERSUBJECT\n\n")

    for n in notes:
        pitch = "empty" if n.is_empty else n.pitch
        f.write(f"{pitch} {note_duration_names[n.duration]}\n")

    f.write("\n")


def get_final_cadence(key, is_major):
    scale_degrees = major_degrees if is_major else minor_degrees
    offset = keys_indexes[key]
    dominant = [scale_degrees[4] + offset, scale_degrees[6] + offset, scale_degrees[1] + offset]
    tonic = [scale_degrees[0] + offset, scale_degrees[2] + offset, scale_degrees[4] + offset]
    return dominant, tonic


def get_melody_in_range(notes: [Note], note_range):
    lowest_note_value = 128
    highest_note_value = -1
    low_bound = note_value[note_range[0]]
    high_bound = note_value[note_range[1]]

    for note in notes:
        if note.pitch != 0 or not note.is_empty:
            if note.pitch > highest_note_value:
                highest_note_value = note.pitch
            if note.pitch < lowest_note_value:
                lowest_note_value = note.pitch

    # offset by octaves (divisible by 12) to not change the key
    # get offset, can be outside of range but try to minimise difference
    offset = (low_bound - lowest_note_value) // 12 * 12
    if offset < 0:
        offset += 12
    elif offset > (high_bound - highest_note_value):
        offset = (high_bound - highest_note_value) // 12 * 12
    print(offset)
    fitted_notes = []
    for note in notes:
        new_pitch = note.pitch if note.pitch == 0 else note.pitch + offset
        fitted_notes.append(Note(new_pitch, note.duration))

    # TODO for user experience check for invalid pitch values (must be from 0 to 127)
    return fitted_notes


def parse_structure(file_path: str):
    file = open(file_path)
    lines = file.read().splitlines()

    # first line is for keys involved
    keys = lines[0].split()
    parts = []

    for line in lines[1:]:
        parts.append(line.split())

    return keys, parts


def build_fugue(subject_file: str, structure_file: str):
    keys, parts = parse_structure(structure_file)

    s_file = open(subject_file)
    subject = Subject(s_file)
    ranges = get_melody_ranges(len(parts))

    # prepare countersubjects
    distinct_cs = set()
    countersubjects_notes = []

    for piece in parts[0]:
        if piece[0] == 'C' and piece[1] == 'S':
            distinct_cs.add(piece)

    while len(distinct_cs):
        if len(countersubjects_notes) == 0:
            cs = generate_counterpoint(subject.notes)
            countersubjects_notes.append(cs)
        else:
            cs = generate_counterpoint(countersubjects_notes[-1])
            countersubjects_notes.append(cs)
        distinct_cs.pop()

    for cs in countersubjects_notes:
        write_notes(cs)

    tracks_notes = []
    for part in parts:
        tracks_notes.append([Note(0, 120, True)])

    empty_part_duration = get_total_duration(subject.notes)

    for idx, key in enumerate(keys):
        modulation_function = lambda x: x
        if key == "D":
            modulation_function = modulate_to_dominant
        elif key == "R":
            key, is_major = get_key_formatted_from_notes(subject.notes)
            modulation_function = lambda notes: modulate_to_relative(notes, key, is_major)
        elif key == "DR":
            key, is_major = get_key_formatted_from_notes(subject.notes)
            modulation_function = lambda notes: modulate_to_dominant(modulate_to_relative(notes, key, is_major))
        elif key == "SD":
            modulation_function = modulate_to_subdominant

        for voice_idx, part in enumerate(parts):
            print(part[idx])
            if part[idx] == "S":
                # subject
                # modulate here
                modulated_notes = modulation_function(subject.notes)
                fitted_notes = get_melody_in_range(modulated_notes, ranges[voice_idx])
                tracks_notes[voice_idx].extend(fitted_notes)
            elif part[idx] == "A":
                # answer
                # modulate
                modulated_notes = modulation_function(subject.notes)
                fitted_notes = get_melody_in_range(modulated_notes, ranges[voice_idx])
                tracks_notes[voice_idx].extend(fitted_notes)
            elif "CS" in part[idx]:
                # countersubject
                # pick from cs list
                cs_index = int(part[idx][-1]) - 1
                # modulate
                modulated_notes = modulation_function(countersubjects_notes[cs_index])
                # fit in range
                fitted_notes = get_melody_in_range(modulated_notes, ranges[voice_idx])
                # add to track
                tracks_notes[voice_idx].extend(fitted_notes)
            elif part[idx] == "FC":
                # free counterpoint
                # generate
                fc = generate_counterpoint(countersubjects_notes[-1])
                # modulate
                modulated_notes = modulation_function(fc)
                # fit
                fitted_notes = get_melody_in_range(modulated_notes, ranges[voice_idx])
                tracks_notes[voice_idx].extend(fitted_notes)
            elif part[idx] == "E":
                # empty space
                tracks_notes[voice_idx].append(Note(0, empty_part_duration, True))

    key, is_major = get_key_formatted_from_notes(subject.notes)
    dominant, tonic = get_final_cadence(key, is_major)
    ranges = get_melody_ranges(len(tracks_notes))
    for idx, track in enumerate(reversed(tracks_notes)):
        duration = note_duration['quarter']
        melody: [Note]
        if idx < 3:
            melody = [Note(dominant[idx], duration), Note(tonic[idx], duration)]
        else:
            melody = [Note(random.choice(dominant), duration), Note(random.choice(tonic), duration)]
        melody = get_melody_in_range(melody, ranges[len(tracks_notes) - idx - 1])
        track.extend(melody)

    return tracks_notes


def get_midi_tracks(tracks_list: [[Note]]):
    midi_tracks = []
    for track in tracks_list:
        messages_list = []
        for note in track:
            messages_list.extend(note.get_midi_messages())
        midi_tracks.append(MidiTrack(messages_list))

    return midi_tracks


def export_fugue(midi_tracks: [MidiTrack]):
    file = MidiFile(type=1)
    meta_track = MidiTrack()
    meta_track.append(MetaMessage('time_signature', numerator=4, denominator=4, clocks_per_click=24, notated_32nd_notes_per_beat=8, time=0))
    meta_track.append(MetaMessage('set_tempo', tempo=600000, time=0))
    file.tracks.append(meta_track)
    file.ticks_per_beat = 240

    for track in midi_tracks:
        file.tracks.append(track)

    file.save("outputs/output.midi")
