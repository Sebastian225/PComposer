import random

from mido import Message
from constants import *


class Note:
    """
    Basic note functionalities\n
    pitch: midi pitch \n
    duration: in ticks
    """
    def __init__(self, pitch: int, duration: int, is_empty=False):
        self.pitch = pitch
        self.duration = duration
        self.is_empty = is_empty

    def get_midi_messages(self, velocity=127):
        if self.is_empty:
            velocity = 0
        return [Message('note_on', channel=0, note=self.pitch, velocity=velocity, time=0),
                Message('note_off', channel=0, note=self.pitch, velocity=velocity, time=self.duration)]


class Subject:
    """create a subject from a file"""

    def __init__(self, file):
        self.notes = []
        for line in file:
            note = line.split()
            self.notes.append(Note(note_value[note[0]], note_duration[note[1]], note[0] == "empty"))


def modulate(notes: [Note], key_from, key_to, direction):
    """
    returns a list of notes in another key\n
    key names should not contain b, only #\n
    direction should be "up" or "down"
    """
    offset = keys_indexes[key_to] - keys_indexes[key_from]
    if direction == "down":
        offset -= 12
    if key_to == key_from and direction == "up":
        offset = 12
    transposed_notes = []
    for note in notes:
        new_note = Note(note.pitch + offset, note.duration)
        transposed_notes.append(new_note)
    return transposed_notes


def modulate_to_dominant(notes: [Note], direction):
    return modulate(notes, "C", "G", direction)


def modulate_to_relative(notes: [Note], key, is_major: bool):
    offset_from_c = keys_indexes[key]
    notes_degrees = [(x.pitch - offset_from_c) % 12 for x in notes]
    octaves = [x.pitch // 12 - 1 for x in notes]
    relative_key_offset = 5 if is_major else 2
    scale_degrees = major_degrees if is_major else minor_degrees
    scale_degree_to_index = major_degrees_to_index if is_major else minor_degrees_to_index
    new_notes = []

    for i, degree in enumerate(notes_degrees):
        # print(degree)
        index = scale_degree_to_index[degree] + relative_key_offset
        if index >= 7:
            octaves[i] += 1
            index = index % 7
        new_notes.append(Note(scale_degrees[index] + offset_from_c + 12 * octaves[i], notes[i].duration))

    return new_notes


class Answer:
    def __init__(self, subject: Subject, is_real: bool):
        if is_real:
            self.notes = modulate_to_dominant(subject.notes, "down")


# def generate_counterpoint(notes: [Note], key: str, is_major: bool):
#     consonant_intervals = [2, 4, 5, 7]  # indexes offset for third, fifth, sixth and octave intervals
#     degrees = major_degrees if is_major else minor_degrees
#     # degrees_to_index = major_degrees_to_index if is_major else minor_degrees_to_index
#     degrees_to_index = major_degrees_to_index | minor_degrees_to_index  # maybe this is a fix for the todo
#     result = []
#
#     beats = []
#     current_ticks = 0
#     beat_notes = []
#     for note in notes:
#         current_ticks += note.duration
#         beat_notes.append(note.pitch)
#         if current_ticks >= note_duration["quarter"]:
#             surplus = current_ticks - note_duration["quarter"]
#             beats.append(beat_notes)
#             beat_notes = []
#             current_ticks = 0
#             for i in range(surplus // note_duration["quarter"]):
#                 beats.append([note.pitch])
#             if surplus % note_duration["quarter"]:
#                 current_ticks + surplus % note_duration["quarter"]
#                 beat_notes.append(note.pitch)
#
#     chosen_intervals = []
#     for beat in beats:
#         chosen_interval = random.choice(consonant_intervals)
#         while chosen_intervals != [] and chosen_intervals[-1] == chosen_interval and (
#                 chosen_interval == 4 or chosen_interval == 7):
#             # if we get parallel fifths or octaves we pick again
#             chosen_interval = random.choice(consonant_intervals)
#         while len(chosen_intervals) > 3 and chosen_intervals[-1] == chosen_intervals[-2] == chosen_intervals[-3] == chosen_interval and (chosen_interval == 2 or chosen_interval == 5):
#             # don't allow 4 consecutive thirds or sixths
#             chosen_interval = random.choice(consonant_intervals)
#         chosen_intervals.append(chosen_interval)
#         important_note = beat[0] if beat[0] != 0 else beat[1]
#         important_note -= keys_indexes[key]
#         # TODO: daca nota nu exista in gama? gen B in C minor
#         abstract_note = important_note % 12
#         # next_octave_offset is for when we get a note that would be in the next octave
#         # if we don't have that, the harmony would jump to the bottom of the octave, and we don't want that
#         next_octave_offset = 0
#         if (degrees_to_index[abstract_note] + chosen_interval) >= 7:
#             next_octave_offset = 12
#         harmonised_degree = degrees[(degrees_to_index[abstract_note] + chosen_interval) % 7]
#         harmonised_pitch = important_note - abstract_note + harmonised_degree + next_octave_offset
#         result.append(Note(harmonised_pitch, note_duration["quarter"]))
#
#     print(beats)
#     return result


