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

    def get_midi_messages(self, velocity=64):
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
    transposed_notes = []
    for note in notes:
        new_note = Note(note.pitch + offset, note.duration)
        transposed_notes.append(new_note)
    return transposed_notes


def modulate_to_dominant(notes: [Note], direction):
    return modulate(notes, "C", "G", direction)


class Answer:
    def __init__(self, subject: Subject, is_real: bool):
        if is_real:
            self.notes = modulate_to_dominant(subject.notes, "down")
