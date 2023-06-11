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
        pitch = self.pitch
        if self.is_empty:
            velocity = 0
            pitch = 0
        if pitch < 0:
            pitch = 0
        return [Message('note_on', channel=0, note=pitch, velocity=velocity, time=0),
                Message('note_off', channel=0, note=pitch, velocity=velocity, time=int(self.duration))]


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
        new_note = Note(note.pitch + offset, note.duration, note.is_empty)
        transposed_notes.append(new_note)
    return transposed_notes


def modulate_to_dominant(notes: [Note]):
    return modulate(notes, "C", "G", "down")


def modulate_to_subdominant(notes: [Note]):
    return modulate(notes, "C", "F", "down")


def modulate_to_relative(notes: [Note], key, is_major: bool):
    offset_from_c = keys_indexes[key]
    notes_degrees = [(x.pitch - offset_from_c) % 12 for x in notes]
    octaves = [x.pitch // 12 - 1 for x in notes]
    relative_key_offset = 5 if is_major else 2
    scale_degrees = major_degrees if is_major else minor_degrees
    scale_degree_to_index = {**major_degrees_to_index, **minor_degrees_to_index}
    new_notes = []

    for i, degree in enumerate(notes_degrees):
        # print(degree)
        index = scale_degree_to_index[degree] + relative_key_offset
        if index >= 7:
            octaves[i] += 1
            index = index % 7
        new_notes.append(Note(scale_degrees[index] + offset_from_c + 12 * octaves[i], notes[i].duration, notes[i].is_empty))

    return new_notes


class Answer:
    def __init__(self, subject: Subject, is_real: bool):
        if is_real:
            self.notes = modulate_to_dominant(subject.notes)


